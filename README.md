# Symptom Checker AI Chatbot

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)
![React](https://img.shields.io/badge/React-18.2%2B-61DAFB)
![LangChain](https://img.shields.io/badge/LangChain-Integration-purple)

This project is a proof-of-concept conversational AI designed to act as an informational assistant for the symptom "Abdominal pain in adults." It uses a locally-hosted language model (`google/flan-t5-base`) to provide answers and guide users through a series of questions based on a pre-built knowledge base derived from the Mayo Clinic.

**The primary goal of this project is to demonstrate a hybrid chatbot architecture, not to provide medical advice.**

## 💡 Key Features

-   **Hybrid Conversational Model**: The bot operates in two distinct modes:
    1.  **Q&A Mode**: Answers general questions from a comprehensive knowledge base.
    2.  **Guided Mode**: Asks a structured series of questions to help a user explore factors related to their symptoms, mimicking a guided flow.
-   **100% Local**: Runs entirely on your local machine. No need for external API keys for the language model.
-   **Data-Driven**: The knowledge base comes from pre-processed JSON files, ensuring the bot only answers from the data it was trained on.
-   **Clear Medical Disclaimer**: The bot is explicitly designed as an informational tool and consistently reminds users that it is not a substitute for a professional medical diagnosis.

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

-   Python 3.9 or higher
-   Node.js v16+ and npm
-   Git for cloning the repository

### Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```

2.  **Set Up the Backend Server**
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

    # Install the required Python packages
    pip install -r requirements.txt
    ```

3.  **Set Up the Frontend Application**
    *In a new, separate terminal*, navigate to the frontend directory.
    ```bash
    # Navigate to the frontend directory from the project root
    cd frontend

    # Install the required npm packages
    npm install
    ```

### Running the Application

You need two terminals running simultaneously to operate the application.

1.  **Start the Backend API**
    In your backend terminal (with the `venv` activated):
    ```bash
    uvicorn main:app --reload
    ```
    The API will be running at `http://localhost:8000`. Wait for the message indicating the model has loaded.

2.  **Start the Frontend App**
    In your frontend terminal:
    ```bash
    npm start
    ```
    This will automatically open your web browser to `http://localhost:3000`, where you can begin interacting with the chatbot.

## 🛠️ Technology Stack

| Backend                               | Frontend              |
| ------------------------------------- | --------------------- |
| Python                                | React                 |
| FastAPI                               | TypeScript            |
| LangChain                             | Axios                 |
| Transformers & PyTorch                |                       |
| FAISS (for vector search)             |                       |
| `undetected-chromedriver` (for dev)   |                       |

*(Note: The `scraper.py` script used during development to build the JSON knowledge base is included in the repository but is not required for running the application, as the data files are pre-built.)*

---

> ## ⚠️ Medical Disclaimer
>
> **This application is for informational and educational purposes only.** It is not intended to be a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read or interacted with on this application.
