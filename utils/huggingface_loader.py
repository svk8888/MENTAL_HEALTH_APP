"""Hugging Face dataset loader for mental health data"""
from datasets import load_dataset


class HuggingFaceLoader:
    """Loads mental health datasets from Hugging Face"""
    
    def load_mental_health_datasets(self):
        """Load datasets from Hugging Face"""
        documents = []
        
        try:
            # Mental Health Q&A Dataset
           # mental_health_qa = load_dataset("pubmed_qa", "pqa_labeled", split="train[:100]")
            #mental_health_qa

            mental_health_qa = load_dataset("qiaojin/PubMedQA", "pqa_labeled", split="train[:100]")
            for item in mental_health_qa:
                documents.append({
                    "content": f"Question: {item['question']} Answer: {item['long_answer']}",
                    "metadata": {"source": "pubmed_qa", "type": "medical_qa"}
                })
        
        except Exception as e:
            print(f"Hugging Face load failed: {e}")
            # Fallback to local dataset
            documents.extend(self.load_fallback_data())
        
        return documents
    
    def load_fallback_data(self):
        """Fallback data if online sources fail"""
        return [
            {
                "content": "Anxiety management: Practice deep breathing, progressive muscle relaxation, and mindfulness meditation regularly.",
                "metadata": {"source": "fallback", "type": "coping_strategy"}
            },
            {
                "content": "Depression support: Maintain routine, engage in pleasant activities, exercise, and seek social connection.",
                "metadata": {"source": "fallback", "type": "support_advice"}
            }
        ]