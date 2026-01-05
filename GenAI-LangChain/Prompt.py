from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import load_prompt
from pydantic import BaseModel

load_dotenv()

class PromptRequest(BaseModel):
    paper: str
    style: str
    length: str
    difficulty: str | None = None
    format: str | None = None
    focus: str | None = None

app = FastAPI(
    title="LangChain Prompt API",
    description="FastAPI server for LangChain prompts",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


Gemini = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

prompt_template = load_prompt("template.json")


@app.post("/prompt")
def run_prompt(data: PromptRequest):
    # Use PromptTemplate.invoke()
    prompt_value = prompt_template.invoke({
        "paper_input": data.paper,
        "style_input": data.style,
        "length_input": data.length,
        "difficulty_input": data.difficulty or "Not specified",
        "format_input": data.format or "Standard explanation",
        "focus_input": data.focus or "General overview",
    })

    # Pass PromptValue directly to Gemini
    response = Gemini.invoke(prompt_value)
    return {"response": response.content}