import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("HF_TOKEN")

####################### Text Generation ###############################
# from agents.textEndPoint import ResearchAssistant

# assistant = ResearchAssistant(api_key=api_key)

# # Define a topic
# topic = "The impact of AI on climate change research"

# # Generate response
# response = assistant.generate_response(topic)

# # Print the output
# print("************************************")
# print(response['text'])

from agents.imageEndPoint import ImageOCR

ocr = ImageOCR()
text = ocr.extract_text(r"C:\Users\madha\Pictures\Jeff-Bezos-PNG-HD-Isolated.png")
print(text)
