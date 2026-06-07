import json
from mcp_client import create_client
from litellm import completion  # Supports OpenAI, Anthropic, Gemini, etc.



class ChatCore:
    def __init__(self, model_name="gpt-4o"):
        self.model_name = model_name

    async def handle_user_request(self, user_prompt: str, session_id: str):
        print(f"[CORE] Received request from Session {session_id}: '{user_prompt}'")

        async with create_client() as client:
            await client.ping()

            # Initialize connection and discover tools
            available_tools = await client.list_tools()
            llm_tools = self._format_mcp_tools_for_llm(available_tools)

            # Step A: Send user prompt + available tools to the LLM
            print("[CORE] Consulting LLM to decide next steps...")
            response = completion(
                model=self.model_name,
                messages=[{"role": "user", "content": user_prompt}],
                tools=llm_tools,
                tool_choice="auto"
            )

            response_message = response.choices[0].message
            tool_calls = response_message.get("tool_calls", [])

            # Step B: Check if the LLM decided it needs to use a tool
            if tool_calls:
                for tool_call in tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    print(f"[CORE] LLM decided to call tool: '{tool_name}' with args: {tool_args}")

                    # Step C: CORE executes the tool via the MCP Server
                    print(f"[CORE] Executing tool '{tool_name}' via MCP Server...")
                    db_result = await client.call_tool(tool_name, arguments=tool_args)

                    # Step D: Send the DB data back to the LLM to get a natural language summary
                    print("[CORE] Feeding database results back to LLM...")
                    final_response = completion(
                        model=self.model_name,
                        messages=[
                            {"role": "user", "content": user_prompt},
                            response_message,
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "name": tool_name,
                                "content": json.dumps(db_result)
                            }
                        ]
                    )
                    
                    # Step E: Return final answer to Chat UI
                    return final_response.choices[0].message.content

            else:
                # The LLM didn't need any tools, just return its conversational answer
                return response_message.content

    def _format_mcp_tools_for_llm(self, mcp_tools):
        """Helper to convert MCP tool definitions into OpenAI/LiteLLM tool schemas"""
        # Hardcoded schema representation for this example script
        return [{
            "type": "function",
            "function": {
                "name": "get_latest_orders",
                "description": "Retrieves the most recent customer orders from the database.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "description": "Number of orders to pull."}
                    },
                    "required": ["limit"]
                }
            }
        }]

# ==========================================
# 3. SIMULATING A CHAT UI UN-AUTHED REQUEST
# ==========================================
import asyncio

async def main():
    core = ChatCore()
    
    # Client UI generates a session ID because there is no Auth login
    anonymous_session_id = "sess_rand_9482b" 
    user_query = "Hey, can you pull up my last 2 orders?"
    
    # Kick off the process
    final_output = await core.handle_user_request(user_query, session_id=anonymous_session_id)
    
    print("\n[Chat UI Display]:")
    print(final_output)

if __name__ == "__main__":
    asyncio.run(main())