"""
Convert HTML plots to PNG files for documentation.
Requires playwright: pip install playwright
After install, run: playwright install
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def save_plot_as_png(playwright, html_path: Path, png_path: Path, viewport: dict):
    """Convert a single HTML plot to PNG."""
    browser = await playwright.chromium.launch()
    page = await browser.new_page(**viewport)
    
    # Load the HTML file
    await page.goto(f'file://{html_path.absolute()}')
    
    # Wait for Plotly to render
    await page.wait_for_selector('.js-plotly-plot', state='visible')
    await page.wait_for_timeout(1000)  # Extra second for animations
    
    # Take the screenshot
    await page.screenshot(path=str(png_path), full_page=True)
    await browser.close()

async def main():
    plots_dir = Path(__file__).parent.parent / 'plots'
    if not plots_dir.exists():
        print(f"No plots directory found at {plots_dir}")
        return
        
    # Configure screenshot size/scale
    viewport = {
        "viewport": {
            "width": 1000,
            "height": 600
        }
    }
    
    html_files = {
        'example_temperature.html': 'example_temperature.png',
        'example_rainfall.html': 'example_rainfall.png'
    }
    
    async with async_playwright() as p:
        for html_name, png_name in html_files.items():
            html_path = plots_dir / html_name
            png_path = plots_dir / png_name
            
            if not html_path.exists():
                print(f"Warning: {html_path} not found")
                continue
                
            print(f"Converting {html_path.name} to {png_path.name}...")
            await save_plot_as_png(p, html_path, png_path, viewport)
            print(f"Saved {png_path.name}")

if __name__ == '__main__':
    asyncio.run(main())