from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType


api_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=500)
WikiTool = WikipediaQueryRun(api_wrapper=api_wrapper)
Websearch = DuckDuckGoSearchRun()


model = ChatOpenAI(model="gpt-4", temperature=0)
tools = [WikiTool, Websearch]

agent = initialize_agent(
    tools=tools,
    llm=model,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)

prompt = "You are a ReaserchAI you have aceess to tools that enables you to do reaserch baised on what user asks, make a proper sumary and give that as an output, you have tools to search on web and also search private vector dbs, Give a summary as output, use proper formating Have Action after Thought  USER : "


def SearchAgent(Input):
    result = agent.invoke(prompt + Input)

    return result

if __name__ == "__main__":
    userQuery = prompt + input("Ask a question: ")
    result = agent.invoke(userQuery)

    print("Agent Replay :", result)
