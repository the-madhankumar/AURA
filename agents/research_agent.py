from typing import List
from rich.pretty import pprint
from pydantic import BaseModel, Field
from phi.agent import Agent, RunResponse
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.newspaper4k import Newspaper4k
from dotenv import load_dotenv
import os

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

model_id = "deepseek-r1-distill-llama-70b"

class ResearchArticle(BaseModel):
    topic: str = Field(..., description="Research topic.")
    sources: List[str] = Field(..., description="List of sources used.")
    summary: str = Field(..., description="Summary of the research findings.")
    insights: str = Field(..., description="Key insights from the research.")

# Web Search Agent
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search for information on the web",
    tools=[DuckDuckGo()],
    model=Groq(id=model_id),
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True,
)

# Research Agent
research_agent = Agent(
    name="Research Agent",
    role="Extract and summarize research articles",
    tools=[Newspaper4k()],
    model=Groq(id=model_id),
    instructions=[
        "For a given topic, search for the top 5 links.",
        "Then read each URL and extract the article text. If a URL isn't available, ignore it.",
        "Analyze and prepare a well-structured article based on the information.",
        "Always include sources.",
    ],
    response_model=ResearchArticle,
    structured_outputs=True,
    show_tool_calls=True,
    markdown=True,
)

# Multi-agent System
multi_ai_agent = Agent(
    team=[web_search_agent, research_agent],
    instructions=["Always include sources", "Ensure the article is well-structured and insightful."],
    show_tool_calls=True,
    markdown=True,
    model=Groq(id=model_id),
)

structured_output_response: RunResponse = multi_ai_agent.run("Simulation theory")
# pprint(structured_output_response.content)


import textwrap

def print_article(text):
    wrapper = textwrap.TextWrapper(width=80)
    for paragraph in text.split("\n"):
        if paragraph.startswith("# "):
            print("\n\033[1;34m" + paragraph + "\033[0m")  
        elif paragraph.startswith("## "):
            print("\n\033[1;32m" + paragraph + "\033[0m") 
        elif paragraph.startswith("### "):
            print("\n\033[1;36m" + paragraph + "\033[0m") 
        elif paragraph.startswith("- ") or paragraph.startswith("* ") or paragraph.startswith("1.") or paragraph.startswith("2.") or paragraph.startswith("3."):
            print("\033[1;33m" + paragraph + "\033[0m")  
        else:
            print(wrapper.fill(paragraph))  

print_article(structured_output_response.content)