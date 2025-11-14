"""Tavily Web Search integration for recent/real-time information"""
import os
from typing import List, Dict, Optional
from tavily import TavilyClient


class TavilyWebSearch:
    """Web search using Tavily API for recent mental health information and real-time data"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Tavily client
        
        Args:
            api_key: Tavily API key (optional, will use TAVILY_API_KEY env var if not provided)
        """
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            print(" Warning: TAVILY_API_KEY not found. Web search will not work.")
            self.client = None
        else:
            self.client = TavilyClient(api_key=self.api_key)
    
    def search(self, query: str, max_results: int = 3) -> List[Dict]:
        """
        Perform web search using Tavily
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with content and metadata
        """
        if not self.client:
            print(" Tavily client not initialized. Skipping web search.")
            return []
        
        try:
            # Perform search
            response = self.client.search(
                query=query,
                max_results=max_results,
                search_depth="advanced",  # More comprehensive search
                include_answer=True,  # Get AI-generated answer from search results
                include_raw_content=False  # Don't need full HTML
            )
            
            results = []
            
            # Add AI-generated answer if available
            if response.get('answer'):
                results.append({
                    "content": f"Web Search Summary: {response['answer']}",
                    "metadata": {
                        "source": "tavily_ai_answer",
                        "type": "web_search_summary"
                    }
                })
            
            # Add individual search results
            for result in response.get('results', [])[:max_results]:
                results.append({
                    "content": f"Title: {result.get('title', 'N/A')}\nContent: {result.get('content', 'N/A')}",
                    "metadata": {
                        "source": result.get('url', 'unknown'),
                        "type": "web_search_result",
                        "title": result.get('title', 'N/A')
                    }
                })
            
            print(f"Tavily search returned {len(results)} results for: {query[:50]}...")
            return results
            
        except Exception as e:
            print(f" Tavily search failed: {e}")
            return []
