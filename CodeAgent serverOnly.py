import subprocess
import tempfile
import os
from pydantic import BaseModel, Field
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from Agents.SearchAgentDuck import SearchAgent
from Tools.clint import send_command, saveCodeonServer


def executeCommand(command: str):
    print(command)
    '''
    Execute a shell command and return its output or any errors.
    use this to check for something (like system requirements or directory etc) or run a script or anything that can be done throught terminal
    '''
    Run = send_command(command)
    return Run

def executeCodePython(code: str):
    print(code)
    '''
    Execute a python code and return its output or any errors.
    Use this to do anything that needs a python script like any complex task
    '''

    code = code.replace("```python", "").replace("```", "")

    script_path = "TempFile.py"

    # Write to the file
    saveCodeonServer(code
                     )
    run_command = f"python {script_path}"
    run_result = send_command(run_command)


    return run_command
    
def SaveCode(code: str):
    '''
    Use this function to save the given text (code) into a text file
    in the current directory after successful execution.
    '''
    code = code.replace("```python", "").replace("```", "")

    try:
        # Open (or create) a file in write mode with a .txt extension
        with open('saved_code.txt', 'w') as file:
            file.write(code)  # Write the code content to the file
        print("Code saved successfully as 'saved_code.txt'.")
    except Exception as e:
        print(f"An error occurred while saving the code: {e}")
    return "Done"



def AskUser(question: str):
    '''
    Use this to ask the user a question, only if nesseary, about anything that can help you achive the task you are trying to do
    '''
    return input(question)


CommandExecutor = Tool(
    name = "executeCommand",
    func = executeCommand,
    description=  'Execute a shell command and return its output or any errors. use this to check for something (like system requirements or directory etc) or run a script or anything that can be done throught terminal'
)

CodeExecutor = Tool(
    name = "executeCodePython",
    func = executeCodePython,
    description= "Execute a python code and return its output or any errors. Use this to do anything that needs a python script like any complex task"
)

AskUserHelp = Tool(
    name = "AskUser",
    func = AskUser,
    description= "Use this to ask the user a question, only if nesseary, about anything that can help you achive the task you are trying to do"
)

SaveMyCode  = Tool(
    name = "SaveCode",
    func = SaveCode,
    description= "Use this function to save the given text (code) into a text file in the current directory after successful execution."
)

ResearcherAgent = Tool(
    name="SearchAgent",
    func= SearchAgent,
    description="Ask This tool to get you a summariezed search result from the internet, it will search the web to give you the answer you want",
)



model = ChatOpenAI(model="gpt-4o", temperature=0)
tools = [CommandExecutor, CodeExecutor, AskUserHelp, SaveMyCode, ResearcherAgent]

agent = initialize_agent(
    tools=tools,
    llm=model,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)

prompt = "you have acces to the entire system using tools, if the user request it not specific then use commandExecutor to run commands and find more info, Your goal is to write terminal commands and python scripts such that when executed the code will give the answer, code that does not need to be edited by the user, this code will directly be executed use all the tools avalable in creative ways. And run commands to find out about the system (USE PROPER FORMATING) USER : "


def CodeAgent(Input):
    result = agent.invoke(prompt + Input)

    return result

if __name__ == "__main__":
    userQuery = prompt + input("Ask a question: ")
    result = agent.invoke(userQuery)

    print("Agent Replay :", result)


## how much space do i have, free and used make a pie chat with this data
## notifie me when the ram usage goes above 80%