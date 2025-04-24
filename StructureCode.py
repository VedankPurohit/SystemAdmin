from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
class ResponseFormatter(BaseModel):
    """Always use this tool to structure your response to the user."""
    thinking: str = Field(description="Plan step by step in detail to answer the user's question")
    answer: str = Field(description="Answer by only giving the code and nothing else")
    Depenecies: str = Field(description="Give all the reuired packages to run this code, only give commands (ex- pip install numpy) and nothing else, make this comma seprated")


# proves that the agent remembers all prev answer in one structure

# class ResponseFormatter(BaseModel):
#     """Always use this tool to structure your response to the user."""
#     answer: str = Field(description="say 4")
#     SameAnswer: str = Field(description="say the same number + 1")


model = ChatOpenAI(model="gpt-4o", temperature=0)
# Bind responseformatter schema as a tool to the model
model_with_tools = model.bind_tools([ResponseFormatter])
# Invoke the model
query = input("Ask a question: ")

ai_msg = model_with_tools.invoke(query)

print(ai_msg.tool_calls[0]["args"])

print(ai_msg.tool_calls[0]["args"]["thinking"])
print(ai_msg.tool_calls[0]["args"]["answer"])
print(ai_msg.tool_calls[0]["args"]["Depenecies"])