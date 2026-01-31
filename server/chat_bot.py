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

    # 1. Extract the raw output (checking both 'output' and 'response' keys)
    raw = result.get("output") or result.get("response")
    
    if not raw:
        return "I'm sorry, I couldn't process that request."

    # 2. Handle cases where the output is a list (common with multi-part tool responses)
    if isinstance(raw, list):
        text_parts = []
        for item in raw:
            if isinstance(item, dict) and "text" in item:
                text_parts.append(item["text"])
            elif isinstance(item, str):
                text_parts.append(item)
        # Join the parts into one clean string
        return "".join(text_parts).strip()

    # 3. Handle the case where it's already a string
    return str(raw).strip()

# Test it out
print(chat("Hello"))
print(chat("should I buy apple today?"))

# chat1 = chat("Hii")
# print(chat1)
# # {'response': ["Hello! I'm your AI stock analysis assistant. Please tell me which stock you'd like to know about, and I'll fetch the latest market analysis for you.\n"]}
# chat2 = chat("Hii, can you tell me should I buy or sell Amazon's stock?")
# print(chat2)
# {'response': [{'type': 'text', 'text': 'Given the current **VOLATILE** market regime and a **HIGH** risk level, the recommendation is to **HOLD** Amazon stock. This verdict', 'extras': {'signature': 'CiQBcsjafKPGIH8n/kMZRnoNPWe8aywaAKCcW+TkFCBWnq1eyq8KbwFyyNp834WxVY6PKvqPH5GrxGGHCWvRWf1mNhR4eGEawb7XvFFUjhK9y4IWRufUNv6WxDYLHv5QtiLUqwrEQMoJeifHQ5o/wHHuxh8JkD0RliVyhpe4JAHoCoEubKi6QObKCtB/q91pr0J7Tz5cswq1AQFyyNp8iTn0+apgt0Dzu3nMDN2CQPZkP47VztO4Q88/lsAhTgC0cP0aF2qIMfuH99OkEAmMF+0X0KtlBUmXoBy+dZkuTyLTFnyUL5pyrYmJjaroW86p3/d1zVP98ItUQja7iOvq4bLfwBkm+UOwFw+Fwc4UUj0nM1uffPA+qF5vZ1y2vKN8z5TQrvEDdqWQ6bt6sXBNpha5GUrF+jwDWHsrKByotbpPrwsYldLwWVNzaDLOu3qX2XZCPe8S4c8nRBfwC61pUloesAB1NyF7cClnxypF/fYDQpDcATMAsD3Ihw5Yby8MDapERh05BiTL9PeMy9ToaTF99PDqGpeXiFqn/d7na2bYnBU+7f1a0hLiQjtuyxCvzV02exTDYBDBetbaFjbHGDUrDG+pa9yT7sTAI9dGsMjx+4pLqeIZs+dxtHzDs0qCcU5kmAPG0vQZrQ/Dq7P14ApWAXLI2nyecf7ubhlagAB6RuVpoW37bQa5l2WXWYN5ywS0eoqKEJMYT1DTIaAaI8qMUw/LqdFBmV8gq1z++W3ImgoiBPFSXlsrLNnLkbdV7Dt8I1IB+e0='}, 'index': 0}, ' comes with a high confidence level of 79%, primarily due to elevated volatility and significant disagreement among market participants.'