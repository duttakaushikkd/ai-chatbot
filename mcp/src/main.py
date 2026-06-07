import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from fastmcp import FastMCP

mcp = FastMCP("Demo", host="0.0.0.0", port=8090)
BACKEND_API_BASE = "http://127.0.0.1:8080"

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


def fetch_latest_orders(limit: int):
    query = urlencode({"limit": limit})
    request = Request(f"{BACKEND_API_BASE}/api/orders?{query}", headers={"Accept": "application/json"})
    with urlopen(request) as response:
        payload = json.load(response)
    return payload.get("orders", [])

@mcp.tool()
def get_latest_orders(limit: int) -> list:
    """Fetch latest orders by routing through backend APIs."""
    return fetch_latest_orders(limit)

if __name__ == "__main__":
    mcp.run(transport="sse")
