import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

# Add ai-core source directory to import path so the backend can import chat router.
ROOT_DIR = Path(__file__).resolve().parents[2]
AI_CORE_SRC = ROOT_DIR / "ai-core" / "src"
if str(AI_CORE_SRC) not in sys.path:
    sys.path.insert(0, str(AI_CORE_SRC))

from chat import router as chat_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

static_path = ROOT_DIR / "frontend"
if static_path.exists():
    app.mount("/", StaticFiles(directory=str(static_path), html=True), name="frontend")

app.include_router(chat_router)

@app.get("/api/orders")
async def get_orders(limit: int = 5):
    sample_orders = [
        {"order_id": "A100", "amount": 39.99, "status": "shipped"},
        {"order_id": "A101", "amount": 84.50, "status": "processing"},
        {"order_id": "A102", "amount": 15.75, "status": "delivered"},
        {"order_id": "A103", "amount": 129.00, "status": "shipped"},
        {"order_id": "A104", "amount": 22.10, "status": "pending"},
    ]
    return {"orders": sample_orders[:limit]}

@app.get("/hello")
async def hello():
    return {"message": "Hello World"}

@app.get("/greet/{name}")
async def greet(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/items")
async def get_items():
    return {"items": ["item1", "item2", "item3"]}

@app.post("/items")
async def create_item(item: dict):
    return {"message": "Item created", "item": item}

@app.get("/cities")
async def get_cities():
    return {"cities": ["city1", "city2", "city3"]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
