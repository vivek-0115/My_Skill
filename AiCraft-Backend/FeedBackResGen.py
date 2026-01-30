from langchain_classic.schema.runnable import RunnableBranch, RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from pydanticClass import FeedbackRequest, FeedbackResponse, SentimentResult
from models import MiniMax
from fastapi import APIRouter

# Define Output Parsers
stringParser = StrOutputParser()
sentimentResultParser = PydanticOutputParser(pydantic_object=SentimentResult)
feedbackResponseParser = PydanticOutputParser(pydantic_object=FeedbackResponse)

# Creating Router Instance
router = APIRouter(prefix="/api")

sentimentAnalysisPrompt = PromptTemplate(
    template="""Classify the sentiment of the following feedback.

                Feedback:
                {feedback}
                
                {format_instruction}
        """,
    input_variables=['feedback'],
    partial_variables={'format_instruction': sentimentResultParser.get_format_instructions()}
)

positiveFeedbackPrompt = PromptTemplate(
    template="""Write a polite, appreciative, and professional response to the following positive feedback in about 30 words.

                Feedback:
                {feedback}

                {format_instruction}
        """,    
    input_variables=['feedback'],
    partial_variables={'format_instruction': feedbackResponseParser.get_format_instructions()}
)

negativeFeedbackPrompt = PromptTemplate(
    template="""Write a polite, empathetic, and constructive response to the following negative feedback in about 30 words.

                Feedback:
                {feedback}

                {format_instruction}
        """,
    input_variables=['feedback'],
    partial_variables={'format_instruction': feedbackResponseParser.get_format_instructions()}
)

neutralFeedbackPrompt = PromptTemplate(
    template="""Write a polite and neutral response to the following feedback in about 30 words.        

                Feedback:
                {feedback}

                {format_instruction}
        """,
    input_variables=['feedback'],
    partial_variables={'format_instruction': feedbackResponseParser.get_format_instructions()}
)

getSentimentChain = sentimentAnalysisPrompt | MiniMax | sentimentResultParser

getResponseChain = RunnableBranch(
    (
        lambda x: x.sentiment == 'positive',
        positiveFeedbackPrompt | MiniMax | feedbackResponseParser,
    ),
    (
        lambda x: x.sentiment == 'negative',
        negativeFeedbackPrompt | MiniMax | feedbackResponseParser,
    ),
    (
        lambda x: x.sentiment == 'neutral',
        neutralFeedbackPrompt | MiniMax | feedbackResponseParser,
    ),
    RunnableLambda(lambda x: {
        'sentiment': 'Could not determine sentiment', 
        'response': 'Unable to generate response due to unclear sentiment.'
        })
)

generateResponseChain = getSentimentChain | getResponseChain

@router.post("/feedback-response-generator", response_model=FeedbackResponse)
def generate_feedback_response(data: FeedbackRequest):

    res = generateResponseChain.invoke({
        'feedback': data.feedback
    })
    return FeedbackResponse(
        sentiment=res.sentiment,
        response=res.response
    )