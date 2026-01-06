from pydantic import BaseModel, Field
from typing_extensions import Literal

class PromptRequest(BaseModel):
    paper: str
    style: str
    length: str
    difficulty: str | None = None
    format: str | None = None
    focus: str | None = None

class FeedbackRequest(BaseModel):
    feedback: str

class SentimentResult(BaseModel):
    sentiment: Literal['positive', 'negative', 'neutral'] = Field(
        description="Sentiment of the feedback. Must be 'positive', 'negative', or 'neutral'."
    )

class FeedbackResponse(BaseModel):
    sentiment: Literal['positive', 'negative', 'neutral'] = Field(description="Sentiment of the feedback.")
    response: str = Field(description="Generated response to the feedback.")