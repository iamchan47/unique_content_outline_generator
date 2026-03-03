import os
import sys
import threading
from dotenv import load_dotenv
from scanner import SERPScanner
from generator import OutlineGenerator
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.markdown import Markdown
from rich.table import Table

# Initialize Rich Console
console = Console()

def main():
    # Load Environment Variables
    load_dotenv()
    
    # Check for keys (or ask for them if missing)
    # Note: In a production CLI tool, you'd want to handle this gracefully
    google_api_key = os.getenv('GOOGLE_API_KEY')
    serper_api_key = os.getenv('SERPER_API_KEY')

    # Display Welcome Banner
    console.print(Panel.fit(
        "[bold blue]SEO Content Outline AI[/bold blue] 🚀\n"
        "[dim]Analyze top 10 organic results and build the ultimate SEO roadmap.[/dim]",
        border_style="blue"
    ))

    if not google_api_key or not serper_api_key:
        console.print("[bold red]Error:[/bold red] Missing API Keys! Please add GOOGLE_API_KEY and SERPER_API_KEY to your .env file.")
        console.print("\n[dim]Visit: https://aistudio.google.com/app/apikey (Google AI)[/dim]")
        console.print("[dim]Visit: https://serper.dev/ (Serper.dev for Google Search)[/dim]")
        return

    # Get User Query
    if len(sys.argv) > 1:
        keyword = " ".join(sys.argv[1:])
    else:
        keyword = console.input("[bold green]Enter the target Keyword/Topic: [/bold green]")

    if not keyword.strip():
        console.print("[red]Please enter a valid keyword.[/red]")
        return

    # Initialize Modules
    scanner = SERPScanner(serper_api_key)
    generator = OutlineGenerator(google_api_key)

    # Multi-step Progress
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        
        # Task 1: Fetch SERP
        serp_task = progress.add_task("[cyan]Fetching Google SERP (Top 10 Organic)...", total=10)
        organic_results = scanner.fetch_top_10(keyword)
        
        if not organic_results:
            console.print("[bold red]Failed to fetch SERP results. Check your Serper API key or connection.[/bold red]")
            return

        progress.update(serp_task, completed=10)

        # Task 2: Scrape Competitors
        scrape_task = progress.add_task("[yellow]Analyzing & Scraping Competitor Content...", total=len(organic_results))
        
        competitors_context = ""
        for idx, res in enumerate(organic_results, 1):
            url = res.get('link')
            title = res.get('title')
            
            progress.update(scrape_task, description=f"[yellow]Scraping ({idx}/{len(organic_results)}): {title[:40]}...")
            
            site_content = scanner.scrape_content(url)
            competitors_context += f"--- SITE {idx}: {title} (URL: {url}) ---\n"
            competitors_context += site_content[:4000] # Increased context window
            competitors_context += "\n\n"
            
            progress.advance(scrape_task)

        # Task 3: AI Analysis & Generation
        ai_task = progress.add_task("[magenta]Synthesizing Data & Generating Optimized Outline via AI...", total=1)
        final_outline = generator.generate(keyword, competitors_context)
        progress.update(ai_task, completed=1)

    # FINAL REPORT
    console.print("\n" + "="*80)
    console.print(f"[bold green]✨ AI Content Outline Ready for: [/bold green] [bold white]{keyword}[/bold white]")
    console.print("="*80 + "\n")
    
    # Display Markdown Result
    md_result = Markdown(final_outline)
    console.print(md_result)

    # Save to File
    filename = f"outline_{keyword.lower().replace(' ', '_')}.md"
    # Ensure filename is safe
    import re
    filename = re.sub(r'[^\w\-_\.]', '', filename)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(final_outline)
    
    console.print(f"\n[bold blue]💾 Saved to: [/bold blue] {filename}")
    console.print("\n[bold yellow]Ready to upload to GitHub![/bold yellow] 🚀")

if __name__ == "__main__":
    main()
