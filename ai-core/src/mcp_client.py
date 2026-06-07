import asyncio
import os
from fastmcp import Client


def create_client():
    """Create and return an MCP client.

    Defaults to a local MCP server at http://127.0.0.1:8090.
    Use MCP_SERVER_URL to connect to a different MCP HTTP/SSE server.
    """
    mcp_url = os.environ.get("MCP_SERVER_URL", "http://127.0.0.1:8090")
    return Client(mcp_url)


async def main():
    async with create_client() as client:
        # Basic server interaction
        await client.ping()

        # List available operations
        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()

        # Execute operations
        result = await client.call_tool("add", {"a": 5, "b": 3})
        print(result)

if __name__ == "__main__":
    asyncio.run(main())