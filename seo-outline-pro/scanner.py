import requests
from bs4 import BeautifulSoup
import os
from typing import List, Dict, Optional
import urllib3

# Suppress SSL warnings for robustness during scraping
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SERPScanner:
    def __init__(self, serper_api_key: str):
        self.api_key = serper_api_key
        self.headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

    def fetch_top_10(self, query: str) -> List[Dict]:
        """Fetch top 10 organic search results from Google via Serper.dev"""
        url = "https://google.serper.dev/search"
        payload = {
            "q": query,
            "num": 10
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            results = response.json()
            return results.get('organic', [])[:10]
        except Exception as e:
            print(f"Error fetching SERP results: {e}")
            return []

    def scrape_content(self, url: str) -> str:
        """Scrape text content and headings from a given URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Remove scripts, styles, etc.
            for script_or_style in soup(["script", "style", "nav", "footer", "header"]):
                script_or_style.decompose()
            
            # Extract headings specifically as they are vital for outlines
            extracted_text = []
            for tag in soup.find_all(['h1', 'h2', 'h3', 'p']):
                text = tag.get_text(strip=True)
                if len(text) > 20: # Filter out noise
                    extracted_text.append(f"[{tag.name}] {text}")
            
            return "\n".join(extracted_text)
        except Exception as e:
            # We silently fail individual scrapes but report it to the user
            return f"Error scraping {url}: {str(e)}"

    def build_competitor_context(self, organic_results: List[Dict]) -> str:
        """Analyze all top 10 sites and build a massive context string for AI"""
        full_context = ""
        for idx, res in enumerate(organic_results, 1):
            url = res.get('link')
            title = res.get('title')
            print(f"    - Analyzing [{idx}/10]: {title}")
            
            content = self.scrape_content(url)
            full_context += f"--- SITE {idx}: {title} (URL: {url}) ---\n"
            full_context += content[:1500] 
            full_context += "\n\n"
            
        return full_context
