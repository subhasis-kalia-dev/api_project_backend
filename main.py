import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv # Import for loading .env files
 
load_dotenv()

 
app = FastAPI(
    title="Intelligent Web Summarizer API",
    description="Backend service for scraping a URL and generating a 7-point summary using OpenAI."
)

 
origins = [
    "http://localhost:5173",  # Your local React development server
    "http://127.0.0.1:8000", # Your local FastAPI development server (optional, but safe)
    # ----------------------------------------------------
    # NEW PRODUCTION URL: This allows your live Netlify site to connect
    "https://subhasisapi.netlify.app", 
    # ----------------------------------------------------
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI Client
try:
    client = OpenAI()
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    

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
        soup = BeautifulSoup(response.text, "lxml")

        # Remove all <a> tags (links and anchor text)
        for a_tag in soup.find_all("a"):
            a_tag.decompose()

        # Extract only the visible text
        text_only = soup.get_text(separator="\n", strip=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during HTML parsing or cleaning: {e}")

 
    try:
         
        llm_response = client.chat.completions.create(
            model="gpt-5",
            messages=get_messages(text_only)
        )
        summary_text = llm_response.choices[0].message.content

        # 4. Return the result
        return {"summary": summary_text}

    except Exception as e:
        print(f"OpenAI API Call Error: {e}")
        # Handle API key issues, rate limits, or other LLM errors
        raise HTTPException(status_code=500, detail="Failed to generate summary from AI. Please check API key and service status.")

# --- RUNNING INSTRUCTIONS ---
# To run this file locally, save it as 'main.py' and execute in your terminal:
# 1. pip install python-dotenv
# 2. Create a file named .env with the line: OPENAI_API_KEY='your-api-key'
# 3. uvicorn main:app --reload --host 0.0.0.0 --port 8000
