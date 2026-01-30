from pydanticClass import ChatRequest, ChatMessage, ChatResponse, RecentChatsResponse, ChatMessagesResponse, ChatItem, NewChatResponse
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from fastapi import APIRouter, HTTPException, status, Query, Request
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, Annotated
from langchain_core.messages import AIMessageChunk
from sse_starlette.sse import EventSourceResponse
from langgraph.graph import add_messages
from models import Gemini, Mistral
from dotenv import load_dotenv
import asyncio
import sqlite3
import logging
import uuid
import os

logger = logging.getLogger(__name__)
load_dotenv()

os.environ['LANGSMITH_PROJECT'] = "Chatbot-Flow"

conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)
CHAT_REQUEST_CACHE = dict()

# Define State
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

llmModel = Gemini

# Graph Node
def Chat(state: ChatState):
    messages = state["messages"]
    full_content = ""
    try:
        for chunk in llmModel.stream(messages):
            if chunk.content:
                full_content += chunk.content
                yield {"messages": [AIMessageChunk(content=chunk.content)]}

        yield {"messages": [AIMessage(content=full_content)]}
    except Exception as e:
        print("Error inside Chat node", str(e))

# Build Graph
chatGraph = StateGraph(ChatState)
chatGraph.add_node("chat", Chat)
chatGraph.add_edge(START, "chat")
chatGraph.add_edge("chat", END)
chatWorkflow = chatGraph.compile(checkpointer=checkpointer)

# Router
router = APIRouter(prefix="/api/chatbot-flow")

threadId = ""

@router.get("/new-chat", response_model=NewChatResponse)
def new_chat():
    global threadId
    threadId = str(uuid.uuid4())

    return {
        "success": True,
        "tid": threadId,
        "title": f"Chat-{threadId[:8]}"
    }

@router.get("/recent-chats", response_model=RecentChatsResponse)
def get_recent_chats():
    seen_threads = set()
    ordered_threads = []
    
    for checkpoint in list(checkpointer.list(None)):
        config = checkpoint.config.get("configurable", {})
        thread_id = config.get("thread_id")

        if not thread_id:
            continue

        if thread_id not in seen_threads:
            seen_threads.add(thread_id)
            ordered_threads.append(thread_id)

    return RecentChatsResponse(
        success=True,
        data=[
            ChatItem(
                id=thread_id,
                title=f"Chat-{thread_id[:8]}"
            )
            for thread_id in ordered_threads
        ]
    )

@router.get("/chats", response_model=ChatMessagesResponse)
def get_chat_messages(tid: str = Query(...)):
    global threadId
    threadId = tid
    snapshot = chatWorkflow.get_state(
        config={"configurable": {"thread_id": threadId}}
        )

    messages = snapshot.values.get("messages", [])

    formatted_messages = []

    for msg in messages:
        if isinstance(msg, HumanMessage):
            role = "user"
        elif isinstance(msg, AIMessage):
            role = "assistant"
        else:
            continue  # skip system / tool messages if any

        formatted_messages.append({
            "role": role,
            "content": msg.content
        })

    return {
        "success": True,
        "data": {
            "tid": threadId,
            "messages": formatted_messages
        }
    }

@router.post("/chat/message", response_model=ChatResponse)
def chat_message(data: ChatRequest):
    request_id = str(uuid.uuid4())

    CHAT_REQUEST_CACHE[request_id] = {
        "tid": data.tid,
        "query": data.query
    }

    return ChatResponse(success=True, request_id=request_id)

@router.get("/chat/stream")
async def chat_stream(request_id: str):

    request_data = CHAT_REQUEST_CACHE.pop(request_id, None)
    if not request_data:
        return {"error": "Invalid request_id"}

    tid = request_data["tid"]
    query = request_data["query"]

    async def event_generator():
        try:
            CONFIG = {
                "configurable": {"thread_id": tid},
                }

            for message_chunk, metadata in chatWorkflow.stream(
                {"messages": [HumanMessage(content=query)]},
                config=CONFIG,
                stream_mode="messages"
            ):
                if message_chunk.content:
                    yield {
                        "event": "token",
                        "data": message_chunk.content
                    }

                await asyncio.sleep(0)

            yield {"event": "done", "data": ""}

        except Exception:
            logger.exception("Streaming failed")
            yield {"event": "error", "data": "Streaming failed"}

    return EventSourceResponse(event_generator())
