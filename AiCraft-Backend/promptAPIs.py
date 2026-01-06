from fastapi import APIRouter
from langchain_core.prompts import load_prompt

# Import from pydanticClass.py
from pydanticClass import PromptRequest

# Imports from models.py
from models import Gemini

# Creating Router Instance
router = APIRouter(prefix="/api")

prompt_template = load_prompt("template.json")

@router.post("/prompt")
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