import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from dotenv import load_dotenv
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

# Define the tool
@tool(description="Get stock data from backend JSON")
def get_data(stock_name: str) -> dict:
    with open("./data.json", "r") as file:
        data = json.load(file)
    return {
        "stock_name": stock_name,
        "data": data
    }

# Create tools list
tools = [get_data]

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an AI stock analysis assistant. When users ask about stocks, 
    use the get_data tool to fetch the latest market analysis. 
    Provide clear investment recommendations based on the market regime, verdict action, 
    confidence level, and risk assessment. Be concise and explain the reasoning."""),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Main function
def chat(user_message: str):
    result = agent_executor.invoke({"input": user_message})
    return {
        "response": result["output"]
    }