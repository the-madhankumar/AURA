import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("HF_TOKEN")

from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint

class ResearchAssistant:
    def __init__(self, api_key, model="Qwen/QwQ-32B", max_length=512, temperature=0.7):
        self.api_key = api_key
        self.llm = HuggingFaceEndpoint(
            repo_id=model,
            max_length=max_length,
            temperature=temperature,
            huggingfacehub_api_token=api_key
        )
        self.prompt_template = PromptTemplate.from_template(self._get_template())

    def _get_template(self):
        return """
        **Topic:** {topic}

        **Overview:**  
        Briefly introduce the topic and its significance.  

        **Background:**  
        Summarize relevant historical and theoretical context.  

        **Key Insights:**  
        Highlight major findings, studies, or data points.  

        **Analysis:**  
        Evaluate perspectives, advantages, limitations, and debates.  

        **Conclusion & Future Scope:**  
        Summarize key takeaways and suggest future research directions.  

        **Response:**  
        """

    def generate_response(self, topic):
        llm_chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
        return llm_chain.invoke({"topic": topic})

# Example Usage
if __name__ == "__main__":
    assistant = ResearchAssistant(api_key)
    topic = "The impact of AI on climate change research"
    response = assistant.generate_response(topic)
    print("************************************")
    print(response)
