from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from pydanticClass import UserInput
from dotenv import load_dotenv
from fastapi import FastAPI
import asyncio
import uuid

load_dotenv()

app = FastAPI(
    title="Backend System for AiCraft",
    description="FastAPI server for AiCraft Backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Type", "Cache-Control", "Connection"],
)


from promptAPIs import router as prompt_router
app.include_router(prompt_router)

from FeedBackResGen import router as feedback_router
app.include_router(feedback_router)

from univerManageApi import router as univer_manage_router
app.include_router(univer_manage_router)

from WeatherSenseAi import router as weather_sense_ai
app.include_router(weather_sense_ai)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AiCraft Backend System!"}

# Testing SSE
process_store = {}
@app.post("/process")
async def start_process(data: UserInput):
    pid = str(uuid.uuid4())
    process_store[pid] = data.text
    return {"process_id": pid}

@app.get("/process/{pid}")
async def stream_process(pid: str):
    user_text = process_store.get(pid)
    if not user_text:
        return {"error": "Invalid process id"}

    async def generator():
        yield {"data": "Received input"}
        yield {"data": f"Text length = {len(user_text)}"}

        await asyncio.sleep(2)
        yield {"data": "Analyzing..."}

        await asyncio.sleep(2)
        words = user_text.split()
        yield {"data": f"Word count = {len(words)}"}

        await asyncio.sleep(1)
        yield {"event": "done", "data": "Processing complete"}

    return EventSourceResponse(generator())