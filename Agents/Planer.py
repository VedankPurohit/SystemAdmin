from langchain_community.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from CodeAgent import CodeAgent, AskUserHelp
from SearchAgentDuck import SearchAgent


CoderAgent = Tool(
    name="CodeAgent",
    func=CodeAgent,
    description="Send Queries about the system that you want to know,, Dont write commands or code , ask it to do thing in natural language this tool will run terminal commands and code to get you want you need",
)

ResearcherAgent = Tool(
    name="SearchAgent",
    func= SearchAgent,
    description="Ask This tool to get you a summariezed search result from the internet, it will search the web to give you the answer you want",
)

model = ChatOpenAI(model="gpt-4o", temperature=0)
tools = [CoderAgent, ResearcherAgent, AskUserHelp]

agent = initialize_agent(
    tools=tools,
    llm=model,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)

prompt = "You are    the planer, you need to lay out a plan for any task given by the user, you can use search and also run commands to find out more about user system if needed, You will be given System Automation related tasks you need to plan it out such that it will then be given to an devloper who can only write python code or commands in terminal to achieve the task, so plan according to that. and they will use this plan as a plan of action. (Use the tools provided to make the best plan specific the the user needs, Only create the plan, dont try to solve the problem itself, dont go above and beyond the scope of the task only plan to do what the user has asked to do ) use proper formating /n User: "
userQuery = prompt + input("Ask a question: ")


result = agent.invoke(userQuery)

print("Agent Replay :", result)
