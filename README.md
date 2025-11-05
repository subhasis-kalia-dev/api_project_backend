🤖 AI Web Summarizer 🌐

Live Demo & Source Code

Component	Link
🚀 LIVE DEMO	Netlify Status
💻 FRONTEND REPO	GitHub Repo
⚙️ BACKEND REPO	GitHub Repo
✨ Features

State-of-the-Art Summarization: Leverages GPT-4o mini for fast, high-quality, and cost-effective AI summaries.
High-Performance API: Built with FastAPI to ensure fast, asynchronous handling of I/O-heavy web scraping and API calls.
Intelligent Content Extraction: Uses Beautiful Soup to clean HTML and extract only the relevant, human-readable text for the LLM.
Decoupled Architecture: Separate Frontend (React on Netlify) and Backend (FastAPI on Render) for scalability and maintainability.
Cost-Effective: Utilizing Netlify and Render free tiers for hosting to keep operations at zero cost.
🛠️ Tech Stack

Type	Technology	Badge
Backend	Python	Python
API Framework	FastAPI	FastAPI
Frontend	React	React
AI/LLM	GPT-4o mini	OpenAI
Web Scraping	Beautiful Soup	BeautifulSoup
Deployment (FE)	Netlify	Netlify
Deployment (BE)	Render	Render
⚙️ Architecture and Data Flow

The application follows a simple but robust microservice architecture:

Client Request: User inputs a URL on the React frontend.
API Call: The React app sends a POST request with the URL to the deployed FastAPI backend endpoint.
Scraping: The FastAPI server uses a combination of requests and Beautiful Soup to fetch the webpage and parse the HTML, stripping away boilerplate (navbars, ads, etc.) to get the core text content.
AI Processing: The cleaned text is sent to the OpenAI API with a system prompt optimized for concise summarization, utilizing the gpt-4o-mini model.
Response: The final summary from the LLM is sent back to the React frontend, where it is instantly displayed to the user.
🚀 Local Setup Guide

Prerequisites

Python 3.10+
Node.js and npm
An OpenAI API Key
1. Backend Setup (FastAPI - api_project_backend)

Clone the Backend Repo:

git clone [BACKEND_REPO_URL]
cd api_project_backend
Setup Environment:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Configure API Key:

Create a file named .env in the root of the backend directory.
Add your OpenAI API Key and the allowed frontend origin (your Netlify domain).
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
FRONTEND_URL="[https://subhasisapi.netlify.app](https://subhasisapi.netlify.app)"
Run the API Server:

uvicorn main:app --reload
The API will be running at http://127.0.0.1:8000.

2. Frontend Setup (React - api_project)

Clone the Frontend Repo:

git clone [FRONTEND_REPO_URL]
cd api_project
Install Dependencies:

npm install
Configure Backend URL:

Create a file named .env in the root of the frontend directory.
Point the React app to your running backend (use your deployed Render URL for production or http://127.0.0.1:8000 for local testing).
REACT_APP_BACKEND_URL=[http://127.0.0.1:8000/api/summarize](http://127.0.0.1:8000/api/summarize) 
# OR your deployed Render URL
Run the Frontend:

npm start
The app will open in your browser, typically at http://localhost:3000.

