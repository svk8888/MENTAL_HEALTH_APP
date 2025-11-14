import chromadb
from typing import List, Dict
from utils.huggingface_loader import HuggingFaceLoader
from utils.web_loader import WebDataLoader
#from utils.pdf_loader import PDFLoader
#from utils.api_loader import APIDataLoader

class MentalHealthRAG:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./mental_health_db")
        self.collection = self.client.get_or_create_collection("mental_health_knowledge")
        
        # Initialize data loaders
        self.web_loader = WebDataLoader()
        self.hf_loader = HuggingFaceLoader()
        self.load_dynamic_knowledge()
    
    def load_dynamic_knowledge(self):
        """Load data from multiple dynamic sources"""
        if self.collection.count() == 0:
            print("🔄 Loading dynamic mental health knowledge...")
            
            all_documents = []
            all_metadatas = []
            all_ids = []
            doc_id = 0
            
            # 1. Web Scraping
            web_docs = self.web_loader.scrape_mental_health_resources()
            for doc in web_docs:
                all_documents.append(doc["content"])
                all_metadatas.append(doc["metadata"])
                all_ids.append(f"web_{doc_id}")
                doc_id += 1
            
            # 2. Hugging Face Datasets
            hf_docs = self.hf_loader.load_mental_health_datasets()
            for doc in hf_docs:
                all_documents.append(doc["content"])
                all_metadatas.append(doc["metadata"])
                all_ids.append(f"hf_{doc_id}")
                doc_id += 1
            
            # Load into vector DB
            if all_documents:
                self.collection.add(
                    documents=all_documents,
                    metadatas=all_metadatas,
                    ids=all_ids
                )
                print(f"✅ Loaded {len(all_documents)} documents from dynamic sources")
            else:
                print("⚠️ No documents loaded - using fallback")
                self.load_fallback_data()
    
    def retrieve_relevant_content(self, query: str, n_results: int = 3) -> List[Dict]:
        """
        Retrieve relevant mental health content from the vector database
        
        Args:
            query: User's input message
            n_results: Number of relevant documents to retrieve (default: 3)
            
        Returns:
            List of dictionaries containing content and metadata
        """
        try:
            # Check if database has any documents
            if self.collection.count() == 0:
                print("⚠️ Vector DB is empty. LLM will respond without RAG context.")
                return []
            
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Check if any results were returned
            if not results['documents'][0]:
                print("⚠️ No matching documents found in Vector DB. LLM will respond without RAG context.")
                return []
            
            return [
                {
                    "content": doc,
                    "metadata": meta
                }
                for doc, meta in zip(results['documents'][0], results['metadatas'][0])
            ]
        except Exception as e:
            print(f"❌ Error retrieving from Vector DB: {e}. LLM will respond without RAG context.")
            return []