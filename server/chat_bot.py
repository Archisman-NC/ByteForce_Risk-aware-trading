import json
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

# Define the tool
@tool(description="Get stock data from backend JSON")
def get_data(stock_name: str) -> dict:
    try:
        with open("./data.json", "r") as file:
            data = json.load(file)
        return {
            "stock_name": stock_name,
            "data": data
        }
    except FileNotFoundError:
        return {"error": "data.json not found"}

# Create tools list
tools = [get_data]

# Create agent using LangGraph (modern standard)
agent_executor = create_react_agent(llm, tools)

# Main function
def chat(user_message: str):
    # LangGraph returns a dictionary with 'messages'
    result = agent_executor.invoke({"messages": [("user", user_message)]})
    
    # Extract the last message content (AI response)
    last_message = result["messages"][-1].content
    
    return {
        "response": last_message
    }

# chat1 = chat("should I buy Amazon stock today?")
# print(chat1)
{'response': [{'type': 'text', 'text': 'Given the current **VOLATILE** market regime and **HIGH** risk level, it is recommended to **HOLD**', 'extras': {'signature': 'CmoBcsjafIIrajoz21XGF2mKgW+gCUFft4iqwlrY7qJeDk1Pme5M7RzTHyy1DS9oQ/AEd6ox8MZp18WwboifO5tebF9oBNfw/DdnLbbOgfeiuvwWsFlzqPg+znJfcR+aGeed4ld9a8LRAz/wCsgBAXLI2nwiPPbFiVl4CR31kPR07fshvTRey4wbI0Lz9p09dipe82z8ChPUciTrlZPIsSOsDDzVtBYFJf8CBFl583lcBJx57CIdZl14YU+x9owpB6Djie0QwQP8fim/HMkbdQHF+HKCtN09yJl/brP8JvmF3Wmmh0KT6g/iuZf+kedZR7y5kIfxfsZH1dZ8NiVfG5EzMXL9xdBfUE83bHLray3OXlI/PGVKYZbIqfFcTE5YpXwcYkf/cNoxwW0yr5oFp2INc1duQOcKhgIBcsjafN+gPIn6rC7/2+QwRZVSvE/lALBGhsu5G4E+K9QqURnDo9Ieefoe2vDDXCvosDLZe/rIJgtOqKwVXFAzPr1J/5OehB90GxmuzZisCGDYuYuEH2aKJOhwzTEwAoxIBeFeEe/SrHfSWz80oT4TXr98R7+alFCHq1Lv7iYe7PIzYUoa7zCt/qNmBy7b5tNkaoxiND4LoDCnrh93YT4Gts+UxqnMUZPOFvpZOO6gd623LVbiOyZ21af8XQ3Y1d4K7Y4am4FHAYPWoFc8T7uM03zKHmusWmpHHJ3lTa2WINuncaAa1BerkiLZufA9snDar0yn5RMDvHszIOAm7L5sb3Jn5jaNCp4BAXLI2nzEKfjMR1KtgAuT8xehnjOzGDUE1Grd/VJiehjAHt5SN9d0D7JBDCU5vkRVqzlDk2CNZ0Ucn/yVoh+QeOeB1LKmRmbZ9KJqVWkE9/lqpC7yMCkcxX02an49YP6h5j8Mjl4iAE/hCgpu/ZrEU8ll+K/T6/9q/Q3TXHGVDS++bnEjEMtkGJTjMgvTn/FSqN4AbnE6nANKsVMbLQU='}, 'index': 0}, ' Amazon stock. The confidence level for this verdict is 79%. The primary reason for this recommendation is the elevated volatility in the market and significant disagreement among agents, leading to the decision that execution is not currently allowed.']}

chat1 = chat("Can i buy an amazon stock today")
print(chat1['response'])