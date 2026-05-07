from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bs4 import BeautifulSoup
import re
import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_sync
import json
import os


def load_config(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: Configuration file '{file_path}' not found.")
    except json.JSONDecodeError:
        raise ValueError("Error: Invalid JSON format in configuration file.")


CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
config = load_config(CONFIG_FILE)

app = FastAPI()

class URLRequest(BaseModel):
    url: str

browser = None
context = None

@app.on_event("startup")
async def startup_event():
    global browser, context
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()

@app.on_event("shutdown")
async def shutdown_event():
    global browser
    if browser:
        await browser.close()

async def fetch_website_text(url: str) -> dict:
    page = await context.new_page()
    stealth_sync(page) 
    USERNAME = config.get("USERNAME")
    PASSWORD = config.get("PASSWORD")
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    html_content = await page.content()

    if(url.startswith(config.get("IAM_BASE_URL"))
        and await page.locator("#email").is_visible()
        and await page.locator("#password").is_visible()
        and await page.locator("#loginbtn").is_visible()
        ):
        await page.click("#onetrust-accept-btn-handler")
        await page.fill("#email", USERNAME)
        await page.fill("#password", PASSWORD)
        await page.click("#loginbtn")
        await page.wait_for_load_state("networkidle")
        html_content = await page.content()

    await page.close()
    
    return clean_page(url, html_content)

def clean_page(url: str, html_content) -> dict:
    soup = BeautifulSoup(html_content, 'html.parser')

    for tag in soup(['script', 'style', 'meta', 'link', 'header', 'nav', 'footer', 'aside', 'form', 'button', 'input']):
        tag.decompose()
    
    for tag in soup.find_all():
        tag.attrs = {}
    
    for tag in soup.find_all():
        if not tag.text.strip():
            tag.decompose()
    
    cleaned_html = re.sub(r'\n\s*\n', '\n', str(soup)).strip()
    text_content = "\n".join(line for line in soup.get_text(separator="\n").split("\n") if line.strip())
    
    return {"url": url, "xhtml": cleaned_html, "text": text_content}

@app.post("/fetch_text")
async def fetch_text(request: URLRequest):
    try:
        result = await fetch_website_text(request.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
