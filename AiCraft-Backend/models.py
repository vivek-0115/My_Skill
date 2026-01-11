from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv

load_dotenv()

# Define Gemini model
Gemini = ChatGoogleGenerativeAI(model='gemini-2.5-flash')
GeminiLite = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite')
GeminiLite2 = ChatGoogleGenerativeAI(model='gemini-2.0-flash-lite')


# Define Mistral model
Mistral_LLM = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    temperature=0.7,
    max_new_tokens=700,
)

# Create ChatHuggingFace instance for Mistral
Mistral = ChatHuggingFace(llm=Mistral_LLM)


# Define MiniMax model
MiniMax_LLM = HuggingFaceEndpoint(
    repo_id="MiniMaxAI/MiniMax-M2.1",
    task="text-generation",
    max_new_tokens=1000,
)

# Create ChatHuggingFace instance for MiniMax
MiniMax = ChatHuggingFace(llm=MiniMax_LLM)

# Creating SerpAPI, for browsing and search on web
SerperSearch = GoogleSerperAPIWrapper()