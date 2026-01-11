from pydantic import BaseModel, Field
from typing_extensions import Literal

class UserInput(BaseModel):
    text: str = Field(description="Input text from the user.")

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

class WeatherRequest(BaseModel):
    query: str = Field(description="Query for get weather details, forecasts and alerts.")

class CityDetails(BaseModel):
    name: str = Field(description="Name of the City or Location, from the query for weather details, forecasting and alerts.")
    country: str = Field(description="Country where the city or location is located.")
    state: str = Field(description="State or region where the city or location is located, if applicable.")
    latitude: float = Field(description="Latitude coordinate of the city or location.")
    longitude: float = Field(description="Longitude coordinate of the city or location.")

class LocationName(BaseModel):
    name: str = Field(description="Name of the Location or City, from the query for weather details, forecasting and alerts.")
    msg: str = Field(description="Give a response message based on successfull extraction of name of city or location.")

class GetLoactionToolInput(BaseModel):
    location: str = Field(description="Name of the Location or City to get detailed information.")