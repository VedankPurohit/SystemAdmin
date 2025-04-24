import subprocess
import sys
from typing import List

from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool, initialize_agent, AgentType


###############################################################################
# 1. The Shell Command Tool
###############################################################################
def run_shell_command(command: str) -> str:
    """
    Execute a shell command and return its output or any errors.
    """
    try:
        output = subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT, text=True
        )
        return output
    except subprocess.CalledProcessError as e:
        return f"[shell error]\n{e.output}"


shell_tool = Tool(
    name="shell",
    func=run_shell_command,
    description=(
        "Executes a command in the terminal. Input should be a valid shell command. "
        "Use this to install packages, create/edit files, run scripts, etc. "
        "The output will be the stdout or stderr from the shell."
    ),
)


###############################################################################
# 2. Conversation Memory
###############################################################################
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)


###############################################################################
# 3. The LLM and Agent
###############################################################################
llm = OpenAI(
    temperature=0, 
    model_name="gpt-4o",
)

tools = [shell_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory
)


###############################################################################
# 4. Demo Interaction Loop
###############################################################################
def main():
    print("\n=== LangChain Shell Agent Demo ===\n")
    print("Type 'exit' or 'quit' to leave the chat.\n")

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            sys.exit(0)
        
        # Pass the user's prompt to the agent
        response = agent.run(user_input)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    main()
