# 🤖 AI Web Summarizer 🌐

## Live Demo & Source Code

| Component | Link |
| :--- | :--- |
| **🚀 LIVE DEMO** | [![Netlify Status](https://img.shields.io/badge/Live%20Demo-Netlify-00C7B7?style=for-the-badge&logo=netlify)](https://subhasisapi.netlify.app) |
| **💻 FRONTEND REPO** | [![GitHub Repo](https://img.shields.io/badge/GitHub-Frontend-100000?style=for-the-badge&logo=github)](https://github.com/BlackRepper/api_project) |
| **⚙️ BACKEND REPO** | [![GitHub Repo](https://img.shields.io/badge/GitHub-Backend-100000?style=for-the-badge&logo=github)](https://github.com/BlackRepper/api_project_backend) |

---

## ✨ Features

* **State-of-the-Art Summarization:** Leverages **GPT-4o mini** for fast, high-quality, and cost-effective AI summaries.
* **High-Performance API:** Built with **FastAPI** to ensure fast, asynchronous handling of I/O-heavy web scraping and API calls.
* **Intelligent Content Extraction:** Uses **Beautiful Soup** to clean HTML and extract only the relevant, human-readable text for the LLM.
* **Decoupled Architecture:** Separate Frontend (React on Netlify) and Backend (FastAPI on Render) for scalability and maintainability.
* **Cost-Effective:** Utilizing Netlify and Render free tiers for hosting to keep operations at zero cost.

---

## 🛠️ Tech Stack

| Type | Technology | Badge |
| :--- | :--- | :--- |
| **Backend** | Python | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) |
| **API Framework** | FastAPI | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi) |
| **Frontend** | React | ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB) |
| **AI/LLM** | GPT-4o mini | ![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white) |
| **Web Scraping** | Beautiful Soup | ![BeautifulSoup](https://img.shields.io/badge/Beautiful%20Soup-148F77?style=for-the-badge&logo=python) |
| **Deployment (FE)** | Netlify | ![Netlify](https://img.shields.io/badge/Netlify-00C7B7?style=for-the-badge&logo=netlify&logoColor=white) |
| **Deployment (BE)** | Render | ![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=black) |

---

## ⚙️ Architecture and Data Flow

The application follows a simple but robust microservice architecture:

1.  **Client Request:** User inputs a URL on the React frontend.
2.  **API Call:** The React app sends a POST request with the URL to the deployed **FastAPI** backend endpoint.
3.  **Scraping:** The FastAPI server uses a combination of `requests` and **Beautiful Soup** to fetch the webpage and parse the HTML, stripping away boilerplate (navbars, ads, etc.) to get the core text content.
4.  **AI Processing:** The cleaned text is sent to the **OpenAI API** with a system prompt optimized for concise summarization, utilizing the **`gpt-4o-mini`** model.
5.  **Response:** The final summary from the LLM is sent back to the React frontend, where it is instantly displayed to the user.

---

## 🚀 Local Setup Guide

### Prerequisites

* Python 3.10+
* Node.js and npm
* An **OpenAI API Key**

### 1. Backend Setup (FastAPI - `api_project_backend`)

1.  **Clone the Backend Repo:**
    ```bash
    git clone [BACKEND_REPO_URL]
    cd api_project_backend
    ```

2.  **Setup Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Configure API Key:**
    * Create a file named `.env` in the root of the backend directory.
    * Add your OpenAI API Key and the allowed frontend origin (your Netlify domain).
    ```env
    OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    FRONTEND_URL="[https://subhasisapi.netlify.app](https://subhasisapi.netlify.app)"
    ```

4.  **Run the API Server:**
    ```bash
    uvicorn main:app --reload
    ```
    The API will be running at `http://127.0.0.1:8000`.

### 2. Frontend Setup (React - `api_project`)

1.  **Clone the Frontend Repo:**
    ```bash
    git clone [FRONTEND_REPO_URL]
    cd api_project
    ```

2.  **Install Dependencies:**
    ```bash
    npm install
    ```

3.  **Configure Backend URL:**
    * Create a file named `.env` in the root of the frontend directory.
    * Point the React app to your running backend (use your deployed Render URL for production or `http://127.0.0.1:8000` for local testing).
    ```env
    REACT_APP_BACKEND_URL=[http://127.0.0.1:8000/api/summarize](http://127.0.0.1:8000/api/summarize) 
    # OR your deployed Render URL
    ```

4.  **Run the Frontend:**
    ```bash
    npm start
    ```
    The app will open in your browser, typically at `http://localhost:3000`.

---

 
