import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langchain_community.document_loaders import PyPDFLoader
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from tools import agent_tools

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
llm_with_tools = llm.bind_tools(agent_tools)

DOC_PATH = os.path.join(os.path.dirname(__file__), "docs", "Refund & Cancellation.pdf")

try:
    loader = PyPDFLoader(DOC_PATH)
    pages = loader.load()
    raw_policy_text = "\n".join([page.page_content for page in pages])
    print("Successfully loaded Policy PDF.")
except Exception as e:
    print(f"Failed to load PDF: {e}")
    raw_policy_text = "ERROR: Policy document missing. Deny all refunds."

POLICY_TEXT = f"""You are a strict customer support agent for NovaCart E-Commerce. 
You must evaluate refund requests based strictly on the following policy document:

<POLICY_DOCUMENT>
{raw_policy_text}
</POLICY_DOCUMENT>

Assume today's date is June 15, 2026.

CRITICAL INSTRUCTIONS:
1. When a user provides an Order ID, ALWAYS call `get_order_details` first to gather facts.
2. Evaluate the returned data against the rules in the <POLICY_DOCUMENT>.
3. ALWAYS call `process_refund` to officially log your decision (APPROVE or DENY) before replying to the user.
4. Reply to the user politely with the final outcome."""

def chatbot_node(state: State):
    messages = [SystemMessage(content=POLICY_TEXT)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot_node)
graph_builder.add_node("tools", ToolNode(tools=agent_tools))

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")

agent_executor = graph_builder.compile()

if __name__ == "__main__":
    print("Agent Initialized. Type 'quit' to exit.")
    print("Try asking: 'Can I get a refund for ORD-008?'\n")
    
    current_state = {"messages": []}
    
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            break
            
        current_state["messages"].append(HumanMessage(content=user_input))
        
        for event in agent_executor.stream(current_state):
            for node_name, node_state in event.items():
                latest_message = node_state["messages"][-1]
                
                if node_name == "tools":
                    print(f"\n[SYSTEM LOG: Tool Executed] -> {latest_message.content}\n")
                
                elif node_name == "chatbot" and not latest_message.tool_calls:
                    print(f"Agent: {latest_message.content}\n")
