from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.newspaper4k import Newspaper4k
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from typing import List, Optional

# Load environment variables
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Define model ID
model_id = "deepseek-r1-distill-llama-70b"

# Define Pydantic model for structured research queries
class ResearchQuery(BaseModel):
    topic: str = Field(..., description="The research topic to fetch papers on.")
    publication_year: Optional[int] = Field(None, description="Filter research papers by year (default: latest available).")
    num_papers: int = Field(5, description="Number of papers to return (default: 5).")
    sources: List[str] = Field([], description="List of specific sources to fetch from, if applicable.")
    keywords: List[str] = Field([], description="Additional keywords to refine the search.")

# Function to fetch research data based on structured query
def Research(query: ResearchQuery):
    prompt = f"Find {query.num_papers} research papers on '{query.topic}'"
    
    if query.publication_year:
        prompt += f" published in {query.publication_year}."
    
    if query.sources:
        prompt += f" Limit search to {', '.join(query.sources)}."

    if query.keywords:
        prompt += f" Ensure relevance to: {', '.join(query.keywords)}."

    research_paper_agent = Agent(
        name="Research Paper Agent",
        role="Search for and retrieve research papers",
        tools=[DuckDuckGo()],
        model=Groq(id=model_id),
        instructions=[
            "Search for relevant research papers on the given topic.",
            "Retrieve the full text of each paper.",
            "If a paper isn't accessible, skip it.",
            "Extract key findings, methodologies, and conclusions.",
            "Provide a concise and informative summary.",
            "Always include sources."
        ],
        show_tool_calls=True,
        markdown=True,
        structured_outputs=False,
    )

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
        structured_outputs=False,
        show_tool_calls=True,
        markdown=True,
    )

    multi_ai_agent = Agent(
        team=[research_paper_agent, research_agent],
        instructions=[
            "Ensure the summaries are well-structured and insightful.",
            "Always include source links at the end."
        ],
        show_tool_calls=True,
        markdown=True,
        model=Groq(id=model_id),
    )

    for chunk in multi_ai_agent.run(prompt, stream=True):
        yield str(chunk.content)  # ✅ Ensure streaming works properly
