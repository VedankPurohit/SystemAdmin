from langchain.agents import Tool
import requests


def requests_tool_func(url: str) -> str:
    """Fetch content from the given URL."""
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        return f"Request error: {e}"

requestsUrl_tool = Tool(
    name="requests",
    func=requests_tool_func,
    description="Makes HTTP requests to fetch data from a URL"
)

