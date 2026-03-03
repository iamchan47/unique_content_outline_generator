from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json

# Import our existing scanner and generator
from scanner import SERPScanner
from generator import OutlineGenerator

# Load .env
load_dotenv()

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

# Initialize modules (ensure keys are present)
google_api_key = os.getenv('GOOGLE_API_KEY')
serper_api_key = os.getenv('SERPER_API_KEY')

scanner = SERPScanner(serper_api_key) if serper_api_key else None
generator = OutlineGenerator(google_api_key) if google_api_key else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    keyword = data.get('keyword')
    
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400
    
    if not scanner or not generator:
        return jsonify({"error": "API keys are missing in .env"}), 500
    
    try:
        # Step 1: SERP
        organic_results = scanner.fetch_top_10(keyword)
        if not organic_results:
            return jsonify({"error": "No results found for this keyword."}), 404
        
        # Step 2: Build Context & Scrape
        # For the browser version, let's limit context to keep it fast
        competitors_context = ""
        competitors_list = []
        
        for idx, res in enumerate(organic_results, 1):
            url = res.get('link')
            title = res.get('title')
            snippet = res.get('snippet', '')
            
            competitors_list.append({
                "id": idx,
                "title": title,
                "url": url,
                "snippet": snippet
            })
            
            # Scrape content for AI context (first few only for speed in web demo)
            if idx <= 5: 
                content = scanner.scrape_content(url)
                competitors_context += f"--- SITE {idx}: {title} ---\n{content[:2000]}\n\n"
        
        # Step 3: AI Generate
        final_outline = generator.generate(keyword, competitors_context)
        
        return jsonify({
            "keyword": keyword,
            "competitors": competitors_list,
            "outline": final_outline
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Checking for keys before start
    if not google_api_key or not serper_api_key:
        print("Warning: Missing GOOGLE_API_KEY or SERPER_API_KEY in .env")
        
    app.run(debug=True, port=5001)
