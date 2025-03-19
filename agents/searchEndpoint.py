from sentence_transformers import SentenceTransformer
import chromadb

class SearchManager:
    def __init__(self, chroma_db_path="chroma_db", model_name="all-MiniLM-L6-v2"):
        """Initialize search engine with ChromaDB and embedding model."""
        self.client = chromadb.PersistentClient(path=chroma_db_path)
        self.collection = self.client.get_or_create_collection(name="research_paper")
        self.embedding_model = SentenceTransformer(model_name)

    def search_research_paper(self, query, top_k=5):
        """Search stored research paper chunks using semantic similarity."""
        query_embedding = self.embedding_model.encode([query])

        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=top_k,
        )

        return results["documents"]  # Extract documents from results
