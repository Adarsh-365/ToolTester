# server.py



from fastmcp import FastMCP ,  Context
mcp = FastMCP("Simple tool")


@mcp.tool
def add(a: int, b: int) -> int:

    return a * b



@mcp.tool
def greet(name: str) -> str:
    return f"Hello {name}"



if __name__ == "__main__":

    mcp.run(transport="stdio")



