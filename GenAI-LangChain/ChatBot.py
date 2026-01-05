from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

Gemini = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite')

print("\nGemini Chatbot started. Type 'exit' or press Ctrl+C to quit.\n")

try:
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye 👋")
            break

        response = Gemini.invoke(user_input)
        print("Gemini:", response.content)

except:
    print("\n\nChatbot stopped by user. Goodbye 👋")