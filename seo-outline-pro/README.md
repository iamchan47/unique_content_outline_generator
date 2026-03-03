# SEO Content Outline AI 🚀

A powerful AI tool to generate data-driven content outlines by analyzing the **Top 10 organically ranking websites** on Google SERP. This tool helps you bridge the "content gap" and optimize your articles for maximum visibility.

## ✨ Features

- 🔍 **SERP Analysis**: Automatically identifies the top 10 organic results for any keyword.
- 🕸️ **Smart Scraping**: Extracts headings, subheadings, and key content from competitor pages.
- 🤖 **AI Content Clustering**: Uses Gemini AI to analyze common themes across top results.
- 📝 **Optimized Outline**: Generates a structured SEO-friendly outline with topics, intent analysis, and recommended word count.
- 🎨 **Beautiful CLI**: Interactive terminal interface powered by `Rich`.

## 🛠️ Tech Stack

- **Python 3.14+**
- **Google Generative AI** (Gemini)
- **Serper.dev** / **Search API** (for Google SERP)
- **BeautifulSoup4** (for scraping)
- **Rich** (for professional CLI presentation)

## 🏗️ Getting Started

### 1. Prerequisites
- Get a [AIzaSyAyBSjZtD-dqiSS-z0NHDDuXkSkKehwEwY](https://aistudio.google.com/app/apikey)
- Get a [7ede39d1ee586c7e28d66711d174560071678d3f](https://serper.dev/) (Fast & reliable Google search)

### 2. Installation
```bash
git clone https://github.com/your-username/seo-content-outline-ai.git
cd seo-content-outline-ai
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=AIzaSyAyBSjZtD-dqiSS-z0NHDDuXkSkKehwEwY
SERPER_API_KEY=7ede39d1ee586c7e28d66711d174560071678d3f
```

### 4. Usage
```bash
python main.py "best productivity tools 2024"
```

## 📂 Project Structure

- `main.py`: Entry point for the CLI tool.
- `scanner.py`: Logic for Google search and competitor website scraping.
- `generator.py`: Logic for AI-driven outline synthesis.
- `requirements.txt`: Project dependencies.

## 🤝 Contributing
Contributions are welcome! Please open an issue or pull request for any improvements.

## 📄 License
MIT License
