from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os

class RAGService:
    def __init__(self, api_key):
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        self.vector_store = None
    
    def process_embeddings(self):
        """Create embeddings from processed text files"""
        texts = []
        processed_dir = 'processed/texts'
        
        # Read all text files from the processed/text directory
        for filename in os.listdir(processed_dir):
            if filename.endswith('.txt'):
                with open(os.path.join(processed_dir, filename), 'r', encoding='utf-8') as f:
                    texts.append(f.read())
        
        # Create and save embeddings to processed/embeddings directory
        if texts:  # Only create vector store if we have texts
            self.vector_store = FAISS.from_texts(texts, self.embeddings)
            os.makedirs('processed/embeddings', exist_ok=True)  # Ensure directory exists
            self.vector_store.save_local("processed/embeddings/vector_store")
            return len(texts)
        return 0
    
    def load_vector_store(self):
        """Load the existing vector store"""
        try:
            self.vector_store = FAISS.load_local("processed/embeddings/vector_store", self.embeddings)
            return True
        except Exception as e:
            print(f"Error loading vector store: {e}")
            return False
    
    def similar_search(self, query, k=3):
        """Search for similar documents"""
        if not self.vector_store:
            if not self.load_vector_store():
                return []
        
        try:
            results = self.vector_store.similarity_search(query, k=k)
            return [doc.page_content for doc in results]
        except Exception as e:
            print(f"Error during search: {e}")
            return []