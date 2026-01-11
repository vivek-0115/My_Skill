from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from customTools import getLocationDetailTool, getWeatherDetailApi
from langchain_community.utilities import GoogleSerperAPIWrapper
from pydanticClass import CityDetails, LocationName
from langchain_core.prompts import PromptTemplate
from sse_starlette import EventSourceResponse
from pydanticClass import WeatherRequest
from models import Gemini, GeminiLite
from dotenv import load_dotenv
import asyncio
import uuid
import json


load_dotenv()
search = GoogleSerperAPIWrapper()

from fastapi import APIRouter

# Define Output Parsers
stringParser = StrOutputParser()
getCityParser = PydanticOutputParser(pydantic_object=CityDetails)
getLoacationParser = PydanticOutputParser(pydantic_object=LocationName)

# Creating Router Instance
router = APIRouter(prefix="/api/weatherSense-ai")

getCityNamePrompt = PromptTemplate(
    template="""You are an expert in name entity extraction. 
        Rules:
        - Extract only the city or location name
        - If found → respond as plain text
        - If not found → respond with "UNKNOWN"
        - Do NOT use JSON
        - Do NOT use markdown
        - Do NOT use code blocks
        
        Query: {query}

        Follow the format instructions to provide response:
        {format_instruction}
    """,
    input_variables=['query'],
    partial_variables={'format_instruction': getLoacationParser.get_format_instructions()}
)

getCityDetailPrompt = PromptTemplate(
    template="""You are Geoloacation or Geocoding expert. Follow the Steps:
        1. Analyze the given JSON to extract city or location name.
        2. Get the following details: country, state (if applicable), latitude, longitude.
        3. If you do not know the detail, use provided tools.
        4. Follow the format instructions to provide response:

        Json: {json},

        Format Instructions:
        {format_instruction}
        
    """,

    input_variables=["query"],
    partial_variables={'format_instruction': getCityParser.get_format_instructions()},
)

finalResponsePrompt = PromptTemplate(
    template="""
You are WeatherSense AI.

Combine the provided location data, weather API data, and news into one JSON response that strictly follows the given schema.

Return ONLY valid JSON. No text, no markdown.

Use only the provided inputs.
If a field is unknown, set it to null.

INPUTS:

LOCATION:
{location}

WEATHER:
{weather}

NEWS:
{news_data}

Rules:
- Follow the schema exactly.
- All numbers must be numeric.
- Dates must be ISO-8601 UTC.
- If no alerts exist:
  alerts.active = false
  alerts.severity = "none"
  alerts.hazards = []
- Base risk and recommendations on both weather and news.
""",
    input_variables=["location", "weather", "news_data"]
)


jsonSchema = {
  "location": {
    "name": "string",
    "city": "string",
    "state": "string",
    "country": "string",
    "latitude": "number",
    "longitude": "number",
    "timezone": "string"
  },

  "weather": {
    "current": {
      "temperature_c": "number",
      "feels_like_c": "number",
      "humidity_percent": "number",
      "pressure_hpa": "number",
      "wind_speed_kph": "number",
      "wind_direction": "string",
      "visibility_km": "number",
      "cloud_cover_percent": "number",
      "condition": "string",
      "condition_code": "string",
      "last_updated_utc": "string"
    },

    "today_forecast": {
      "max_temp_c": "number",
      "min_temp_c": "number",
      "rain_probability_percent": "number",
      "expected_condition": "string"
    }
  },

  "alerts": {
    "active": "boolean",
    "severity": "none | minor | moderate | severe | extreme",
    "hazards": [
      {
        "type": "cyclone | flood | heatwave | thunderstorm | heavy_rain | cold_wave | air_quality | wildfire | other",
        "title": "string",
        "description": "string",
        "source": "string",
        "issued_at": "string",
        "valid_until": "string"
      }
    ]
  },

  "news": {
    "summary": "string",
    "sources": [
      {
        "title": "string",
        "url": "string",
        "publisher": "string",
        "published_at": "string"
      }
    ]
  },

  "risk_assessment": {
    "overall_risk": "low | medium | high | extreme",
    "primary_risks": ["string"],
    "secondary_risks": ["string"],
    "confidence": "number"
  },

  "recommendations": {
    "public": ["string"],
    "travel": ["string"],
    "health": ["string"],
    "emergency": ["string"]
  },

  "data_sources": {
    "weather_api": "string",
    "news_api": "string",
    "government_sources": ["string"],
    "last_checked_utc": "string"
  }
}



process_store = {}
@router.post("/start-stream")
async def startWeatherSenseAiStream(data: WeatherRequest):
    pid = str(uuid.uuid4())

    if not data.query or data.query.strip() == "":
        return {"error": "Query cannot be empty"}
    
    process_store[pid] = data.query
    return {
        "message": "WeatherSense AI stream started.",
        "process_id": pid
    }

@router.get("/stream/{pid}")
async def WeatherSenseAiStream(pid: str):

    query = process_store.get(pid)

    if not query:
        return {"error": "Invalid process id"}
    
    async def event_generator():
        
        try:
            # Initial Connection Message
            yield {"data": json.dumps({
                        "message": "WeatherSense AI processing started",
                        "content": ""
                    })}
            await asyncio.sleep(0.1)
            # Step 1: Extract city name
            yield {"data": json.dumps({
                        "message": "Extracting location from query",
                        "content": ""
                    })}
            
            getLocationChain = getCityNamePrompt | GeminiLite | stringParser

            location = getLocationChain.invoke(query)
            await asyncio.sleep(0.1)
            yield {"data": json.dumps({
                        "message": "Location extracted",
                        "content": location
                    })}

            # Step 2: Bind tools
            yield {"data": json.dumps({
                        "message": "Binding tools for location details",
                        "content": getLocationDetailTool.name
                    })}
            llmTool = Gemini.bind_tools([getLocationDetailTool])
            await asyncio.sleep(0.1)
            # Step 3: Prepare tool call
            yield {"data": json.dumps({
                        "message": "Preparing tool call for location details",
                        "content": location
                    })}
            await asyncio.sleep(0.1)
            llmToolChain = getCityDetailPrompt | llmTool
            toolCall = llmToolChain.invoke({"json": location})

            # Step 4: Execute tool
            if toolCall.tool_calls:
                await asyncio.sleep(0.1)
                yield {"data": json.dumps({
                            "message": "Tool call identified",
                            "content": toolCall.tool_calls[0]
                        })}
                
                executeToolChain = getLocationDetailTool | getCityParser
                executeTool = executeToolChain.invoke(
                    toolCall.tool_calls[0]
                )
                await asyncio.sleep(0.1)
                yield {"data": json.dumps({
                            "message": "Location details fetched.",
                            "content": ""
                        })}
                
                # Step 5: Get Weather Details
                await asyncio.sleep(0.1)
                yield {"data": json.dumps({
                            "message": "Fetching weather details",
                            "content": ""
                        })}

                weatherDetails = getWeatherDetailApi(
                    name=executeTool.name,
                    latitude=executeTool.latitude,
                    longitude=executeTool.longitude
                )

                await asyncio.sleep(0.1)
                yield {"data": json.dumps({
                            "message": "Weather details fetched successfully.",
                            "content": weatherDetails
                        })}
                
                # Step 6: Search for latest weather forecast and alerts
                await asyncio.sleep(0.1)
                yield {"data": json.dumps({
                            "message": "Searching for latest weather forecast and alerts",
                            "content": ""
                        })}

                searchQuery = f"""{executeTool.name}, {executeTool.country} latest weather forecast and real-time conditions
                    cyclone warning flood alert heatwave advisory rainfall wind storm humidity temperature
                    site:imd.gov.in OR site:ndma.gov.in OR site:gov OR site:weather.com OR site:accuweather.com OR site:bbc.com/weather
                    """

                result = search.run(searchQuery)

                await asyncio.sleep(0.1)
                yield {"data": json.dumps({
                            "message": "Search completed.",
                            "content": result
                        })}

                # Final Message
                await asyncio.sleep(0.1)
                yield {"data": json.dumps({
                            "message": "Generating final response...",
                            "content": ""
                        })}
                prompt = finalResponsePrompt.invoke({
                    "location": executeTool,
                    "weather": weatherDetails,
                    "news_data": result
                })

                finalResponse = Gemini.with_structured_output(jsonSchema).invoke(prompt)
                
            else:
                yield {"data": "No tool calls were made"}

            await asyncio.sleep(0.1)
            yield {"data": json.dumps({
                        "message": "Response Generated.",
                        "content": finalResponse
                    })}
            await asyncio.sleep(0.1)

        except Exception as e:
            print("Error in WeatherSense AI Stream for PID", pid, ":", str(e))
            yield {"event": "error","data": str(e)}

    return EventSourceResponse(
        event_generator(),
    )   
