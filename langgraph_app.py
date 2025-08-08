#!/usr/bin/env python3
"""
LangGraph application that uses MCP server tools
"""

import os
import asyncio
from typing import List, TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict
from typing import Annotated

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.checkpoint.memory import MemorySaver

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_mcp_adapters.resources import load_mcp_resources
from langchain_mcp_adapters.prompts import load_mcp_prompt
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

class State(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]

server_params = StdioServerParameters(
    command="uv",
    args=["run", "server.py"]
)

async def create_graph(session):
    """Create the LangGraph agent with MCP tools"""
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    tools = await load_mcp_tools(session)
    llm_with_tool = llm.bind_tools(tools)

    # Use a simple system prompt since no MCP prompts are available
    system_prompt = "You are a helpful AI assistant with access to weather, dice rolling, and web search tools. Use these tools when appropriate to help users."
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("messages")
    ])
    chat_llm = prompt_template | llm_with_tool

    def chat_node(state: State) -> State:
        state["messages"] = chat_llm.invoke({"messages": state["messages"]})
        return state

    graph_builder = StateGraph(State)
    graph_builder.add_node("chat_node", chat_node)
    graph_builder.add_node("tool_node", ToolNode(tools=tools))
    graph_builder.add_edge(START, "chat_node")
    graph_builder.add_conditional_edges("chat_node", tools_condition, {"tools": "tool_node", "__end__": END})
    graph_builder.add_edge("tool_node", "chat_node")
    graph = graph_builder.compile(checkpointer=MemorySaver())

    return graph

async def main():
    config = {"configurable": {"thread_id": 1234}}
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Check available tools
            tools = await load_mcp_tools(session)
            print("Available tools:", [tool.name for tool in tools])

            # Use the MCP Server in the graph
            agent = await create_graph(session)
            print("🤖 LangGraph MCP Agent Ready!")
            print("Available tools: weather_search, roll_dice, web_search")
            print("Type 'quit' to exit")
            print()
            
            while True:
                try:
                    message = input("User: ")
                    if message.lower() == 'quit':
                        print("👋 Goodbye!")
                        break
                    
                    if not message.strip():
                        continue
                    
                    print("🤖 Agent is thinking...")
                    response = await agent.ainvoke({"messages": [{"role": "user", "content": message}]}, config=config)
                    print("AI:", response["messages"][-1].content)
                    print()
                    
                except KeyboardInterrupt:
                    print("\n👋 Goodbye!")
                    break
                except Exception as e:
                    print(f"❌ Error: {e}")
                    print()


if __name__ == "__main__":
    asyncio.run(main())