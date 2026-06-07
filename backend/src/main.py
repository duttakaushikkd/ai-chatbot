from fastapi import FastAPI
import uvicorn

app = FastAPI()

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
