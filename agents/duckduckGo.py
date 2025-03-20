from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.newspaper4k import Newspaper4k
from dotenv import load_dotenv
import os

class ResearchSearchAgent:
    def __init__(self):
        """Initialize the research search agent with API keys and models."""
        load_dotenv()
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.model_id = "deepseek-r1-distill-llama-70b"

        # Research Paper Search Agent
        self.research_paper_agent = Agent(
            name="Research Paper Agent",
            role="Search for and retrieve research papers",
            tools=[DuckDuckGo()],
            model=Groq(id=self.model_id),
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

        # Research Summarization Agent
        self.research_agent = Agent(
            name="Research Agent",
            role="Extract and summarize research articles",
            tools=[Newspaper4k()],
            model=Groq(id=self.model_id),
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

        # Multi-Agent System
        self.multi_ai_agent = Agent(
            team=[self.research_paper_agent, self.research_agent],
            instructions=[
                "Ensure the summaries are well-structured and insightful.",
                "Always include sources links also at the end."
            ],
            show_tool_calls=True,
            markdown=True,
            model=Groq(id=self.model_id),
        )

    def search(self, query: str) -> str:
        """
        Perform a research search and return the full text result.

        :param query: The topic to search for.
        :return: The full text of the search response.
        """
        response = self.multi_ai_agent.run(query)
        return response  # Returning only the text output


if __name__ == "__main__":
    # Example Usage
    agent = ResearchSearchAgent()
    user_query = input("Enter your research topic: ")
    result = agent.search(user_query)
    
    print("\n--- Research Results ---\n")
    print(result)
