# ai-chatbot

## Local frontend + backend

The backend now exposes a `POST /chat` endpoint and serves a simple static frontend from `frontend/index.html`.

Run the backend from the workspace root:

```bash
cd backend/src
python main.py
```

Then open:

- `http://localhost:8080`

The page sends the user prompt to `/chat`, and the backend forwards it into `ai-core/src/chat.py`.
