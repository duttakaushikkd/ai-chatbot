from fastmcp import FastMCP

mcp = FastMCP("Demo", host="0.0.0.0", port=8090)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
     mcp.run(transport="sse")