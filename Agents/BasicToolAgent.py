import subprocess
import tempfile
import os
from pydantic import BaseModel, Field
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType


model = ChatOpenAI(model="gpt-4o", temperature=0)
# tools = [CommandExecutor, CodeExecutor, AskUserHelp, SaveMyCode]

agent = initialize_agent(
    tools=tools,
    llm=model,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)

prompt = "You are a ReaserchAI you have aceess to tools that enables you to do reaserch baised on what user asks, make a proper sumary on what was asked and give that as an output "
userQuery = prompt + input("Ask a question: ")


result = agent.invoke(userQuery)

print("Agent Replay :", result)
