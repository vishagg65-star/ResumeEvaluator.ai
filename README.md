# Resume Evaluator AI 🚀

An enterprise-grade, graph-based AI resume analyst that simulates the mind of a professional technical recruiter. Built with **LangGraph**, **FastAPI**, and **Groq**, it provides near-instant, deep contextual analysis of resumes against target job roles.

## ✨ Key Features

-   **Graph-Based Analysis**: Uses a multi-node LangGraph pipeline to independently evaluate skills, experience, projects, and education.
-   **Precision Experience Calculation**: Advanced logic to calculate true professional tenure, accurately handling overlapping roles and filtering out non-professional entries.
-   **High-Speed Processing**: Powered by Llama 3.1 8B on Groq LPUs for lightning-fast results.
-   **Modern Dashboard**: Responsive, dark-themed UI built with Vanilla HTML/JS/CSS (no bloated frameworks).
-   **Recruiter Insights**: Clear scoring, suitability verdicts, and semantic skill matching (beyond simple keywords).
-   **Mobile Friendly**: Fully responsive design for seamless viewing on any device.

## 🛠️ Tech Stack

-   **Backend**: FastAPI, Python, LangGraph, LangChain
-   **AI Foundation**: Groq API (Llama 3.1 8B)
-   **Frontend**: Vanilla HTML5, CSS3 (Modern Flex/Grid), JavaScript (ES6+)
-   **Icons**: Font Awesome 6
-   **Typography**: Inter & Poppins (Google Fonts)

## 🚀 Quick Start

### 1. Prerequisites
-   Python 3.9+
-   A Groq API Key (Get one at [console.groq.com](https://console.groq.com))

### 2. Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd ResumeEvaluator-main

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Create a .env file in the root
GROQ_API_KEY=your_key_here
```

### 3. Run Locally
```bash
# Set PYTHONPATH to root and run from src
$env:PYTHONPATH="."; python src/server.py
```
Visit `http://localhost:8080` in your browser.

## 🌐 Deployment (Vercel)

This project is pre-configured for Vercel Serverless deployment.

1.  Upload the root folder to a GitHub repository.
2.  Connect the repository to Vercel.
3.  Add the following **Environment Variables** in Vercel:
    -   `GROQ_API_KEY`: Your key.
    -   `PYTHONPATH`: `.`
4.  Deploy!

## 📁 Project Structure

-   `api/`: Vercel serverless functions.
-   `src/`: Core Python logic and LangGraph nodes.
-   `static/`: Frontend assets (HTML, CSS, JS).
-   `requirements.txt`: Project dependencies.
-   `vercel.json`: Vercel configuration.

---
Created with ❤️ by **Vishal Aggarwal**
