import typer
from rich.prompt import Prompt
from phi.agent import Agent
from phi.knowledge.pdf import PDFKnowledgeBase, PDFReader
from phi.vectordb.chroma import ChromaDb
from phi.embedder.sentence_transformers import SentenceTransformersEmbedder

# Initialize the embedder
embedder = SentenceTransformersEmbedder()

# Initialize the vector database (ChromaDB)
vector_db = ChromaDb(collection="pdf_embeddings", embedder=embedder)

# Initialize the PDF Knowledge Base
pdf_knowledge_base = PDFKnowledgeBase(
    path=r"C:\Users\madha\Pictures\GATE.pdf",  # Folder where your PDFs are stored
    vector_db=vector_db,
    reader=PDFReader(chunk=True),  # Enable chunking for better embeddings
)

# Load PDFs into the knowledge base (Run once)
pdf_knowledge_base.load(recreate=False)  # Set `recreate=True` only for first time

print("📄 PDFs have been successfully embedded into the knowledge base!")


def chat_with_pdf(user: str = "User"):
    """Chat with the embedded PDF knowledge."""
    agent = Agent(
        user_id=user,
        knowledge_base=pdf_knowledge_base,
        use_tools=True,
        show_tool_calls=True,
        debug_mode=True,
    )

    print(f"\n🤖 AI Assistant is ready to chat with the PDFs!\n")
    
    while True:
        message = Prompt.ask(f"[bold] 🗣 {user} [/bold]")  # Take user input
        if message.lower() in ("exit", "bye", "quit"):
            print("👋 Exiting chat. Goodbye!")
            break
        response = agent.generate_response(message)  # Get AI response
        print(f"\n🤖 [bold]AI:[/bold] {response}\n")  # Print response


if __name__ == "__main__":
    typer.run(chat_with_pdf)
