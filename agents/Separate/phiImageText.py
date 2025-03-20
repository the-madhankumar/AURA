from phi.agent import Agent
from phi.model.openai import OpenAIChat
from pathlib import Path

# Initialize the Agent with a vision-capable model
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    markdown=True,
)

# Define the image path
image_path = Path(r"C:\Users\madha\Pictures\Cocaine4.jpg")

# Ensure the image file exists
if not image_path.exists():
    raise FileNotFoundError(f"Image not found at {image_path}")


# Send request
agent.print_response("Write a 3 sentence fiction story about the image",images=[str(image_path)], stream=True)


##   ##  #####   ##   ##
##   ##  #   #   ##   ##
##   ##  #   #   ##   ##
#######  #   #   #######
     ##  #   #        ##
     ##  #   #        ##
     ##  #####        ##
