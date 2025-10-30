import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# REMOVED: from dotenv import load_dotenv
# REMOVED: load_dotenv() - This is not needed in Render as it uses environment variables directly.

# Initialize OpenAI Client (It will automatically look for OPENAI_API_KEY in the environment)
try:
    # client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY")) # Explicitly use os.environ.get if needed
    client = OpenAI() # The default initialization is usually enough
except Exception as e:
    # On Render, if this fails, the OPENAI_API_KEY is missing or invalid.
    print(f"Error initializing OpenAI client: {e}")
    # We allow the app to start, but the /summarize endpoint will crash if the key is bad.


app = FastAPI(
    title="Intelligent Web Summarizer API",
    description="Backend service for scraping a URL and generating a summary using OpenAI."
)

origins = [
    "http://localhost:5173",  # Your local React development server
    "http://127.0.0.1:8000", # Your local FastAPI development server
    "https://subhasisapi.netlify.app", # Production Netlify frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Model for Request Body ---
class SummaryRequest(BaseModel):
    url: str

 
SYSTEM_PROMPT = """
You are an expert content summarizer.
Your task is to read the provided webpage text and produce a clear, concise summary.

Guidelines:
Present the summary as a single, cohesive paragraph of around 300 words.
Capture the main ideas, insights, and key facts from the text.
Use clear, factual language — avoid opinions, filler phrases, or subjective commentary.
Exclude advertisements, unrelated information, navigation menus, or repetitive content.
Maintain logical flow and coherence, ensuring the paragraph reads naturally and smoothly.
Focus only on the core content and meaning of the text.
Do not use bullet points, lists, or headings — produce one well-structured paragraph only.
"""

USER_PROMPT_PREFIX = """
Here are the contents of a website.
If it includes important information, summarize them too.
"""

def get_messages(content: str):
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_PROMPT_PREFIX + content}
    ]

 
@app.post("/summarize")
async def summarize_website(request: SummaryRequest):
    url = request.url

    # 1. Fetch the page HTML
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Handle connection, DNS, or HTTP error codes (4xx, 5xx)
        raise HTTPException(status_code=400, detail=f"Failed to fetch website content: {e}")

    # 2. Parse and Clean the HTML
    try:
        # Using html.parser instead of lxml just in case lxml causes issues, though both are fine
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove elements that are unlikely to be summary content
        for script_or_style in soup(["script", "style", "header", "footer", "nav"]):
            script_or_style.decompose()

        # Extract only the visible text
        text_only = soup.get_text(separator="\n", strip=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during HTML parsing or cleaning: {e}")

 
    # 3. Call OpenAI LLM
    try:
        llm_response = client.chat.completions.create(
            model="gpt-4o-mini", # Changed to gpt-4o-mini for efficiency/availability
            messages=get_messages(text_only),
            temperature=0.2,
        )
        summary_text = llm_response.choices[0].message.content

        # 4. Return the result
        return {"summary": summary_text}

    except Exception as e:
        print(f"OpenAI API Call Error: {e}")
        # Re-raise the HTTPException with a specific message
        raise HTTPException(status_code=500, detail="AI Summarization failed. Check if API key is valid and has billing enabled.")
