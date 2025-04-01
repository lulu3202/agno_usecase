from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.github import GithubTools
from agno.tools.giphy import GiphyTools
from agno.playground import Playground, serve_playground_app
from agno.storage.agent.sqlite import SqliteAgentStorage

import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

#Web Agent (using DuckDuckGo)
web_agent = Agent(
name="Web Agent",
role="Search the web for information about programming concepts",
model=OpenAIChat(id="gpt-4o"),
tools=[DuckDuckGoTools()],
instructions="Find relevant information on the web. Always include sources.",
show_tool_calls=True,
markdown=True,
)

#GitHub Code Agent
github_agent = Agent(
name="GitHub Code Agent",
role="Find code examples on GitHub",
model=OpenAIChat(id="gpt-4o"),
tools=[GithubTools(search_repositories=True)],
instructions="Find code examples on GitHub related to the user's query. Explain what the code does. Limit to 3 GitHub repo in English",
show_tool_calls=True,
markdown=True,
)

#Giphy Agent
giphy_agent = Agent(
name="Giphy Agent",
role="Find relevant GIFs",
model=OpenAIChat(id="gpt-4o"),
tools=[GiphyTools(
api_key=os.getenv("GIPHY_API_KEY"),
limit=1 # Number of GIFs to return
)],
instructions="Find relevant and appropriate GIFs related to the query.",
show_tool_calls=True,
markdown=True,
)

#Agent Team (managing all three agents)
agent_team = Agent(
team=[web_agent, github_agent, giphy_agent],
model=OpenAIChat(id="gpt-4o"),
instructions=[
"Combine the information from the Web Agent, GitHub Code Agent, and Giphy Agent",
"Present the information in a clear and organized way",
"Include relevant GIFs where appropriate to illustrate concepts",
"Always include sources",
],
show_tool_calls=True,
markdown=True,
)

app = Playground(agents=[web_agent, github_agent, giphy_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground1:app", reload=True)



