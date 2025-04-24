from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools import DuckDuckGoSearchRun

api_wrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=1000)
WikiTool = WikipediaQueryRun(api_wrapper=api_wrapper)

search = DuckDuckGoSearchRun()

# search.invoke("Obama's first name?")

# from langchain_community.tools import DuckDuckGoSearchResults

# search = DuckDuckGoSearchResults()

model = ChatOpenAI(model="gpt-4o", temperature=0)

tools = [
    WikiTool,
    search,]

agent = initialize_agent(
    tools=tools,
    llm=model,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)

prompt = "You are a ReaserchAI you have aceess to tools that enables you to do reaserch baised on what user asks, make a proper detailed report from multiple  on what was asked and give that as an output, you have tools to search on web and also search private vector dbs use the correct format  USER : "


userQuery = prompt + input("Ask a question: ")


result = agent.invoke(userQuery)

print("Agent Replay :", result)
