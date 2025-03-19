from sentence_transformers import SentenceTransformer
import chromadb
import hashlib

class ResearchPaperManager:
    def __init__(self, db_path="chroma_db"):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="research_papers")

    def compute_hash(self, text):
        """Generate a unique hash for a document."""
        return hashlib.sha256(text.encode()).hexdigest()

    def is_duplicate(self, text):
        """Check if the document (or highly similar content) already exists."""
        query_embedding = self.embedding_model.encode([text]).tolist()
        results = self.collection.query(query_embeddings=query_embedding, n_results=1)

        if results["documents"] and results["distances"][0][0] < 0.05:  # Threshold for similarity
            return True  # Duplicate found
        return False

    def add_research_paper(self, text):
        """Add a new research paper if it's not a duplicate."""
        if self.is_duplicate(text):
            print("⚠️ This research paper already exists in the database. Skipping addition.")
            return

        embedding = self.embedding_model.encode([text]).tolist()
        doc_id = self.compute_hash(text)

        self.collection.add(documents=[text], embeddings=embedding, ids=[doc_id])
        print(f"✅ Research paper added with ID: {doc_id}")

