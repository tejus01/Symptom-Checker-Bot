# main.py (Final Hybrid Version)

import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# LangChain and Model components
from langchain.docstore.document import Document
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# Local Hugging Face model components
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain.llms import HuggingFacePipeline
import torch

# --- 1. SETUP THE LOCAL LANGUAGE MODEL (Unchanged) ---
print("Loading local model...")
model_id = "google/flan-t5-base"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=512, device=device)
local_llm = HuggingFacePipeline(pipeline=pipe)
print("Model loaded successfully.")


# --- 2. LOAD AND PROCESS **BOTH** DATA FILES ---
print("Loading and combining all datasets...")
documents = []

# Load the general Q&A data
with open('abdominal_pain_dataset_v2.json', 'r') as f:
    general_data = json.load(f)
for item in general_data:
    content = f"Question: {item['question']}\nAnswer: {item['answer']}"  # 
    documents.append(Document(page_content=content, metadata={'source': 'general_qa'}))

# Load the structured factor data
with open('abdominal_pain_data_final.json', 'r') as f:
    factor_data = json.load(f)
for group in factor_data.get('factor_groups', []):
    group_name = group['group_name']
    factors_list = ", ".join(group['factors'])
    content = f"Regarding the topic '{group_name}', the related factors or characteristics are: {factors_list}."
    documents.append(Document(page_content=content, metadata={'source': 'factor_groups', 'group': group_name}))
emergency_info = factor_data.get('emergency_info')
if emergency_info:
    points_list = "; ".join(emergency_info['points'])
    content = f"Emergency medical care should be sought if: {points_list}"
    documents.append(Document(page_content=content, metadata={'source': 'emergency_info'}))

print(f"Created {len(documents)} combined documents for the knowledge base.")


# --- 3. CREATE VECTOR STORE (For Q&A Mode) ---
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.from_documents(documents, embeddings)
print("Vector store created successfully.")


# --- 4. CREATE THE CONVERSATIONAL CHAIN (For Q&A Mode) ---
retriever = vector_store.as_retriever()
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=local_llm,
    retriever=retriever,
    memory=memory,
    # Using a simpler prompt for the combined data
    combine_docs_chain_kwargs={"prompt": PromptTemplate.from_template(
        "Based on the following context, provide a helpful answer to the question.\n\nContext:\n{context}\n\nQuestion: {question}\n\nHelpful Answer:"
    )}
)


# --- 5. SETUP THE HYBRID BOT LOGIC ---
# For demonstration, we'll use a simple dictionary to store the session state.
user_session = {}

def start_diagnostic_flow():
    """Initializes the diagnostic mode session."""
    user_session['mode'] = 'diagnostic'
    user_session['question_index'] = 0
    user_session['answers'] = []
    # Get the questions from our structured data
    user_session['questions_to_ask'] = factor_data.get('factor_groups', [])
    
def get_next_question():
    """Gets the next question from the diagnostic flow list."""
    idx = user_session.get('question_index', 0)
    questions = user_session.get('questions_to_ask', [])
    if idx < len(questions):
        question_group = questions[idx]
        group_name = question_group['group_name']
        options = ", ".join(question_group['factors'])
        return f"Let's talk about '{group_name}'. Is it any of the following? {options}"
    return None # No more questions

def get_diagnostic_summary():
    """Creates a summary based on the user's answers."""
    # IMPORTANT: This is a simplified summary and NOT a medical diagnosis.
    summary = "Thank you. Based on the information you've provided, you've mentioned factors including: "
    summary += ", ".join(user_session.get('answers', ['none']))
    summary += ". This information can be useful when speaking with a healthcare professional."
    summary += " For more specific advice, you might ask me 'When should I see a doctor?'"
    
    # Reset the session
    user_session.clear()
    return summary


# --- 6. CREATE THE FASTAPI APP ---
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Message(BaseModel):
    text: str

@app.post("/chat")
async def chat(message: Message):
    user_query = message.text.lower()

    # Reset command
    if "start over" in user_query:
        user_session.clear()
        return {"response": "Ok, let's start over. How can I help you?"}
        
    # --- DIAGNOSTIC MODE LOGIC ---
    if user_session.get('mode') == 'diagnostic':
        # Store the previous answer
        user_session['answers'].append(user_query)
        # Increment question index
        user_session['question_index'] += 1
        
        # Ask the next question
        next_question = get_next_question()
        if next_question:
            return {"response": next_question}
        else:
            # If no more questions, provide a summary
            summary = get_diagnostic_summary()
            return {"response": summary}

    # --- TRIGGER FOR DIAGNOSTIC MODE ---
    trigger_phrases = ["help me", "i have pain", "figure out", "my symptoms"]
    if any(phrase in user_query for phrase in trigger_phrases):
        start_diagnostic_flow()
        # Ask the first question
        first_question = get_next_question()
        disclaimer = "I can ask a few questions to help narrow down the factors based on my training data. Please remember, I am an AI assistant and not a medical professional. This is not a medical diagnosis. \n\n"
        return {"response": disclaimer + first_question}

    # --- DEFAULT Q&A MODE ---
    result = qa_chain({"question": user_query})
    return {"response": result['answer']}