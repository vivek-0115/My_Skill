from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI(
    title="Backend System for AiCraft",
    description="FastAPI server for AiCraft Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from promptAPIs import router as prompt_router
app.include_router(prompt_router)

from FeedBackResGen import router as feedback_router
app.include_router(feedback_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AiCraft Backend System!"}