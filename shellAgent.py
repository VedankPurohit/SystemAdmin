from langchain_community.tools import ShellTool

shell_tool = ShellTool()

from langchain.agents import AgentType, initialize_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0)

shell_tool.description = shell_tool.description + f"args {shell_tool.args}".replace(
    "{", "{{"
).replace("}", "}}")
self_ask_with_search = initialize_agent(
    [shell_tool], llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting...")
        break
    else:
        response = self_ask_with_search.run(user_input)
        print(f"Agent: {response}\n")

# self_ask_with_search.run(
#     "Download the langchain.com webpage and grep for all urls. Return only a sorted list of them. Be sure to use double quotes."
# )