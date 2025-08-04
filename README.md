# Symptom Checker AI Chatbot

This project is a conversational AI chatbot designed to act as an informational assistant for the symptom "Abdominal pain in adults." It uses a locally-hosted language model and a knowledge base scraped from the Mayo Clinic's website.

## Features

- **Hybrid Conversational Model**: The bot can operate in two modes:
    1.  **Q&A Mode**: Answers general questions based on a combined knowledge base.
    2.  **Guided Diagnostic Mode**: Asks a series of questions based on structured data to help a user narrow down factors related to their symptoms.
- **Local Language Model**: Runs entirely on your local machine using a `google/flan-t5-base` model, requiring no API keys.
- **Data-Driven**: The knowledge base is built by scraping and parsing data from the Mayo Clinic website.
- **Important Disclaimer**: This bot is an informational tool only and does **not** provide medical advice or diagnosis.

## Technology Stack

- **Backend**:
    - Python
    - FastAPI
    - LangChain (for LLM orchestration)
    - Selenium & BeautifulSoup4 (for web scraping)
    - FAISS (for vector storage)
    - Transformers & PyTorch (for running the local LLM)
- **Frontend**:
    - React with TypeScript
    - Axios

## Setup and Installation

### Prerequisites

- Python 3.9+
- Node.js and npm
- Git

### 1. Backend Setup

First, set up and run the backend server.

```bash
# Navigate to the backend directory
cd backend

# Create and activate a Python virtual environment
# On Windows:
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# Install the required Python packages from requirements.txt
pip install -r requirements.txt

# (Optional) Run the web scraper to generate the latest data
# This will open a browser window and may take a few minutes.
python scraper.py