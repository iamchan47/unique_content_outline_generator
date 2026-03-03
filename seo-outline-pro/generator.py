import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load any local .env if it exists
load_dotenv()

class OutlineGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        # Using gemini-flash-latest for broader stability and free tier compatibility
        self.model_name = 'gemini-flash-latest'
        self.fallback_model = 'gemini-flash-lite-latest'
        self.model = genai.GenerativeModel(self.model_name)

    def generate(self, keyword: str, competitors_context: str) -> str:
        """Analyze top 10 competitor data and generate an optimized content outline"""
        prompt = f"""
        # SEO Expert Analysis & Content Strategy Tool
        
        Keyword: **{keyword}**
        
        Analyze the top 10 organic search results (competitors) for this keyword and generate a comprehensive content outline. 
        Your goal is to help me rank higher by creating a piece of content that is more thorough, 
        covers more user intent, and includes key sections found across the top-ranking pages.
        
        ## Competitor Data Analysis:
        {competitors_context}
        
        ## Your Task:
        1. Identify the common themes across the top 10 ranking sites.
        2. Identify specific "content gaps" or unique insights that we can add to differentiate.
        3. Provide a detailed SEO Content Outline including:
           - Proposed Title (optimized for CTR)
           - Primary & Secondary LSI Keywords
           - Target Search Intent (Informational, Transactional, etc.)
           - Proposed Headings (H1, H2, H3, etc.)
           - Brief notes for each section on what to cover to beat competitors.
           - Estimated word count to be competitive.
        
        Format your response in Markdown with clear sections and professional tone.
        """
        
        try:
            # Drastically reduce context size for free tier token safety
            token_safe_context = competitors_context[:10000] # Safe limit for free tier RPM
            response = self.model.generate_content(prompt.replace(competitors_context, token_safe_context))
            return response.text
        except Exception as e:
            if "429" in str(e) or "Quota exceeded" in str(e):
                # Try fallback model if first one hits limit
                try:
                    self.model = genai.GenerativeModel(self.fallback_model)
                    response = self.model.generate_content(prompt[:5000]) # Even smaller on fallback
                    return "(Using fallback lite model) \n\n" + response.text
                except:
                    return f"Rate limit reached on all models. Please wait 60 seconds. Original error: {str(e)}"
            return f"Error during AI generation: {str(e)}"
