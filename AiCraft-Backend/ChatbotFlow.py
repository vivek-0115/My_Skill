from fastapi import APIRouter, HTTPException, status, Query
from models import Gemini, Mistral
from pydanticClass import ChatRequest, ChatMessage, ChatResponse, RecentChatsResponse, ChatMessagesResponse, ChatItem, NewChatResponse
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import add_messages
import sqlite3
import logging
import uuid

logger = logging.getLogger(__name__)

conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

# Define State
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

llmModel = Gemini

# Graph Node
def Chat(state: ChatState):
    try:
        messages = state["messages"]
        response = llmModel.invoke(messages)
        return {"messages": [response]}
    except Exception as e:
        logger.exception("Error inside Chat node")
        raise RuntimeError("LLM execution failed") from e

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
    
    for checkpoint in reversed(list(checkpointer.list(None))):
        print(checkpoint.config['configurable'])
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

@router.get("/chat", response_model=ChatMessagesResponse)
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


@router.post("/chat", response_model=ChatResponse)
def chat(data: ChatRequest):

    if not data.query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query cannot be empty"
        )

    try:
        initialState = {"messages": [HumanMessage(content=data.query)]}

        CONFIG = {'configurable': {'thread_id': threadId}}
        finalState = chatWorkflow.invoke(initialState, config=CONFIG)

        assistant_message = finalState["messages"][-1]

        return ChatResponse(
            success=True,
            message="Response generated successfully",
            data=ChatMessage(
                role="assistant",
                content=assistant_message.content
            )
        )

    except RuntimeError as e:
        logger.exception("Chat workflow runtime error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI failed to generate a response"
        )

    except Exception as e:
        logger.exception("Unexpected chat error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error"
        )
