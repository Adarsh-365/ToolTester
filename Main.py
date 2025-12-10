import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

config = {
    "demo": {
        "command": "fastmcp",
        "transport": "stdio",
        "args": ["run", "mcptool.py"], 
    }
}

async def main():
    client = MultiServerMCPClient(config)
    
    # 1. Fetch all tools from the connected server(s)
    tools = await client.get_tools()
    
    # Print available tools to see their names
    print(f"Available tools: {[t.name for t in tools]}")

    # 2. Find the 'add' tool specifically
    # Note: Tool names are usually just the function name (e.g., 'add') 
    # unless 'tool_name_prefix' is enabled in the client config.
    add_tool = next((t for t in tools if t.name == "add"), None)

    if add_tool:
        # 3. Call the tool manually using .ainvoke()
        # You must pass arguments as a dictionary
        params = {"a": 10, "b": 5}
        result = await add_tool.ainvoke(params)
        print(result[0]["text"])
        print(f"Calling 'add' with {params}...")
        print(f"Result: {result[0]['text']}") # result is usually a ToolMessage or similar object
    else:
        print("Tool 'add' not found.")

if __name__ == "__main__":
    asyncio.run(main())