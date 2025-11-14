import requests
from bs4 import BeautifulSoup
import time

class WebDataLoader:
    def scrape_mental_health_resources(self):
        """Scrape real-time mental health content"""
        sources = {
            "WHO_mental_health": "https://www.who.int/health-topics/mental-health",
            "NAMI_resources": "https://www.nami.org/About-Mental-Illness/Mental-Health-Conditions",
            "CDC_mental_health": "https://www.cdc.gov/mentalhealth/learn/index.htm"
        }
        
        documents = []
        for source_name, url in sources.items():
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract main content
                content = soup.find('main') or soup.find('article')
                if content:
                    text = content.get_text(strip=True)
                    documents.append({
                        "content": text[:2000],  # Limit length
                        "metadata": {"source": source_name, "type": "web_scraped"}
                    })
                time.sleep(1)  # Be respectful
            except Exception as e:
                print(f"Failed to scrape {url}: {e}")
        
        return documents