import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("HF_TOKEN")
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

research_template = """You are an AI assistant specializing in research. Analyze the given topic carefully and provide a well-structured response.

Topic: {topic}

**Step 1: Introduction**  
Provide a brief overview of the topic and its significance.

**Step 2: Background Information**  
Explain the historical and theoretical context relevant to this topic.

**Step 3: Key Findings and Research Data**  
Summarize the most important discoveries, studies, or relevant data points related to the topic.

**Step 4: Critical Analysis**  
Evaluate different perspectives, advantages, limitations, and any debates surrounding this topic.

**Step 5: Conclusion and Future Directions**  
Summarize the key takeaways and suggest possible future research directions or applications.

Response:
"""

research_prompt = PromptTemplate.from_template(research_template)

question = "The impact of AI on climate change research"

from langchain_huggingface import HuggingFaceEndpoint
repo_id = "Qwen/QwQ-32B"
llm = HuggingFaceEndpoint(repo_id=repo_id, 
                          max_length=128, 
                          temperature=0.7,
                          huggingfacehub_api_token=api_key)

llm_chain = research_prompt | llm
response = llm_chain.invoke({"topic": question})
p= response
print("************************************")
print(p)