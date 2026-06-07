# ai-chatbot

## Architecture

The system is designed to match the following flow:

```
+---------+         (Sends prompt + Session ID)         +--------------------+
| Chat UI | ------------------------------------------> |                    |
+---------+ <------------------------------------------ |                    |
                                     (Final Response)   |                    |
                                                        |  Application Core  |
+---------+         (Tool Call / Context Request)       |  (MCP Host & LLM)  |
|   LLM   | <=========================================> |                    |
+---------+                                             +--------------------+
                                                                  |
                                                                  | (Routes Tool)
                                                                  v
+--------------+            +--------------+            +--------------------+
|   Database   | <========= | Backend APIs | <========= |     MCP Server     |
```

## Components

- `frontend/index.html`
  - Static Chat UI served via the backend.
  - Generates a session ID for each browser session.
  - Sends `prompt` and `session_id` to `POST /chat`.

- `backend/src/main.py`
  - FastAPI host that serves the UI and includes `ai-core`'s chat router.
  - Exposes `/chat` through `ai-core` and an example backend API at `/api/orders`.

- `ai-core/src/chat.py`
  - Acts as the Application Core.
  - Receives chat requests and passes them into `ChatCore.handle_user_request()`.
  - Calls `litellm.completion()` to run the LLM and decide whether a tool is needed.
  - If the LLM requires a tool, it forwards the tool call through MCP.

- `ai-core/src/mcp_client.py`
  - Creates an MCP client to connect to an external MCP server.
  - Defaults to `http://127.0.0.1:8090`.

- `mcp/src/main.py`
  - Separate MCP server process.
  - Exposes tool functions like `add` and `get_latest_orders`.
  - `get_latest_orders` routes to the backend API at `/api/orders`, matching the architecture.

## Request flow

1. Browser UI sends `POST /chat` with `prompt` and `session_id`.
2. The backend app includes `ai-core/src/chat.py` and forwards the request into the Application Core.
3. `ChatCore.handle_user_request()` contacts the external MCP server at `http://127.0.0.1:8090`.
4. The LLM either responds directly or issues a tool call.
5. Tool calls are routed through the MCP server.
6. The MCP server routes tool execution to backend APIs, which can access a database or mocked data source.
7. Result data is returned to the Application Core, and the final text response is sent back to the browser.

## Local run instructions

1. Activate the virtual environment:

```bash
source .venv/bin/activate
```

2. Install dependencies if needed:

```bash
pip install -r backend/src/requirements.txt
pip install -r ai-core/src/requirements.txt
pip install -r mcp/src/requirements.txt
```

3. Start the backend application:

```bash
cd backend/src
python main.py
```

4. Start the MCP server in a separate terminal:

```bash
cd mcp/src
python main.py
```

5. Open the frontend in your browser:

- `http://localhost:8080`

## Notes

- The frontend now sends an explicit `session_id` with each chat request.
- `ai-core/src/chat.py` is the Application Core that hosts the chat flow and MCP orchestration.
- `mcp/src/main.py` is the external MCP server, and it calls the backend API at `/api/orders`.
- The backend API simulates a data source to support MCP tool execution.
- For production use, add authentication, persistent session storage, and a real database.
