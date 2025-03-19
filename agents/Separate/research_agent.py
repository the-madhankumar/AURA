from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.newspaper4k import Newspaper4k
from dotenv import load_dotenv
import os

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

model_id = "deepseek-r1-distill-llama-70b"

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
    structured_outputs=True,
    show_tool_calls=True,
    markdown=True,
)

multi_ai_agent = Agent(
    team=[research_paper_agent, research_agent],
    instructions=[
        "Ensure the summaries are well-structured and insightful.",
        "Always include sources links also at the end."
    ],
    show_tool_calls=True,
    markdown=True,
    model=Groq(id=model_id),
)

# Run the agent
multi_ai_agent.print_response("Artificial Intelligence", stream=True)
