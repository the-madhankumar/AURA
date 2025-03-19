import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb

# Load PDF
def load_pdf(file_path):
    doc = fitz.open(file_path)
    text = "\n".join([page.get_text() for page in doc])
    return text

pdf_text = load_pdf(r"D:\projects\ML AND DL\LungCancer\Assets\MachineLearningApproachofLungCancerPrediction.pdf")

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

chunks = text_splitter.split_text(pdf_text)

print(f"Total Chunks Created: {len(chunks)}")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

chunk_embeddings = embedding_model.encode(chunks, show_progress_bar=True)

print(f"Total Embeddings Created: {len(chunk_embeddings)}")

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="research_paper")

for i, (text, embedding_vector) in enumerate(zip(chunks, chunk_embeddings)):
    collection.add(
        documents=[text],
        embeddings=[embedding_vector.tolist()],
        ids=[str(i)],
    )

def search_research_paper(query):
    query_embedding = embedding_model.encode([query])
    
    results = collection.query(
        query_embeddings=query_embedding.tolist(),  # Convert to list
        n_results=5,
    )
    
    return results["documents"]  

query = "The impact of AI on climate change research"
retrieved_chunks = search_research_paper(query)

for idx, chunk in enumerate(retrieved_chunks[0], 1): 
    print(f"🔹 Chunk {idx}:\n{chunk}\n")
