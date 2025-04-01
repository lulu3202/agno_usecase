import streamlit as st
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.github import GithubTools
from agno.tools.giphy import GiphyTools

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

# Set up the agents

# Web Agent (using DuckDuckGo)
web_agent = Agent(
    name="Web Agent",
    role="Search the web for information about programming concepts",
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    instructions="Find relevant information on the web. Always include sources.",
    show_tool_calls=True,
    markdown=True,
)

# GitHub Code Agent
github_agent = Agent(
    name="GitHub Code Agent",
    role="Find code examples on GitHub",
    model=OpenAIChat(id="gpt-4o"),
    tools=[GithubTools(search_repositories=True)],
    instructions="Find code examples on GitHub related to the user's query. Explain what the code does. Limit to 3 GitHub repos in English.",
    show_tool_calls=True,
    markdown=True,
)

# Giphy Agent
giphy_agent = Agent(
    name="Giphy Agent",
    role="Find relevant GIFs",
    model=OpenAIChat(id="gpt-4o"),
    tools=[GiphyTools(api_key=GIPHY_API_KEY, limit=1)],
    instructions="Find relevant and appropriate GIFs related to the query.",
    show_tool_calls=True,
    markdown=True,
)

# Create Agent Team (handling all three agents)
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

# Streamlit Application
def main():
    st.set_page_config(page_title="Interactive Python Learning Assistant", page_icon="🐍")
    st.title("Interactive Python Learning Assistant")
    st.markdown("""
    ### Enter a Python concept you'd like to learn about!
    This tool will give you:
    - A web-based conceptual explanation
    - Practical code examples from GitHub
    - A visual representation through GIFs
    """)
    
    # User input for the concept they want to learn about
    user_query = st.text_input("Enter your Python concept (e.g., FastAPI, decorators, lambda expressions):")
    
    # Check if the user input is provided
    if user_query:
        # Create placeholders to display the content progressively
        gif_placeholder, concept_placeholder, code_placeholder = st.columns([1, 2, 2])

        # Start the process of getting responses from agents
        if st.button("Learn Now! 🚀"):
            with gif_placeholder:
                st.markdown("### 🎬 Visual Aid (GIF)")
                with st.spinner("Searching for relevant GIF..."):
                    # Collect GIF response using Agent Team
                    response = giphy_agent.run(f"Find a GIF to explain {user_query} concept")
                    gif_placeholder.markdown(response.get_content_as_string())

            with concept_placeholder:
                st.markdown("### 🎯 Conceptual Explanation")
                with st.spinner("Fetching conceptual explanation..."):
                    # Collect Web Agent response
                    response = web_agent.run(f"Explain {user_query} concept clearly with examples")
                    concept_placeholder.markdown(response.get_content_as_string())

            with code_placeholder:
                st.markdown("### 💻 Code Examples from GitHub")
                with st.spinner("Searching for GitHub code examples..."):
                    # Collect GitHub Agent response
                    response = github_agent.run(f"Find Python code examples for {user_query}")
                    code_placeholder.markdown(response.get_content_as_string())

    else:
        st.warning("Please enter a Python concept to learn about!")

if __name__ == "__main__":
    main()
