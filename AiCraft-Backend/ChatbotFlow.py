from fastapi import APIRouter, HTTPException, status
from models import Gemini, GeminiLite
from pydanticClass import ChatRequest, ChatMessage, ChatResponse
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import add_messages
import logging

logger = logging.getLogger(__name__)

# Define State
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Graph Node
def Chat(state: ChatState):
    try:
        messages = state["messages"]
        response = Gemini.invoke(messages)
        return {"messages": [response]}
    except Exception as e:
        logger.exception("Error inside Chat node")
        raise RuntimeError("LLM execution failed") from e

# Build Graph
chatGraph = StateGraph(ChatState)
chatGraph.add_node("chat", Chat)
chatGraph.add_edge(START, "chat")
chatGraph.add_edge("chat", END)
chatWorkflow = chatGraph.compile()

# Router
router = APIRouter(prefix="/api/chatbot-flow")

@router.post("/chat", response_model=ChatResponse)
def chat(data: ChatRequest):

    if not data.query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query cannot be empty"
        )

    try:
        initialState = {
            "messages": [HumanMessage(content=data.query)]
        }

        finalState = chatWorkflow.invoke(initialState)

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
