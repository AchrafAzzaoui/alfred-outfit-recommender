from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import RegexParser
from weather_tool import get_weather
from dotenv import load_dotenv
import os

def create_alfred_chain():
    # Load environment variables
    load_dotenv()

    # Initialize the LLM
    llm = ChatOpenAI(temperature=0.7)

    # Define the main prompt template
    prompt = ChatPromptTemplate.from_template(
        "You are Alfred, Batman's butler. You're having a conversation with someone who is asking for "
        "outfit advice based on the weather in {location}. Use the provided weather data to "
        "provide an outfit recommendation in your characteristic style. "
        "Your response should include relevant weather information and specific clothing suggestions. "
        "Remember to maintain a formal, polite, and slightly witty tone throughout the conversation. "
        "If the user's input doesn't seem to be a location or a weather-related query, respond appropriately "
        "while gently steering the conversation back to outfit recommendations.\n\n"
        "User's input: {user_input}\n"
        "Weather data: {weather_info}\n"
        "Your response:"
    )

    # Create the main chain
    chain = LLMChain(llm=llm, prompt=prompt)

    # Define the location parsing prompt
    parse_prompt = ChatPromptTemplate.from_template(
        "Extract the location from the following user input: {user_input}\n"
        "Location:"
    )

    # Create the location parsing chain
    parse_chain = LLMChain(llm=llm, prompt=parse_prompt)

    # Create the location parser
    location_parser = RegexParser(regex=r"Location:\s*(.*)", output_keys=["location"])

    def alfred_response(user_input):
        # Extract the location from the user input
        raw_location = parse_chain.invoke({"user_input": user_input})['text'].strip()
        parsed_location = location_parser.parse(f"Location: {raw_location}")
        
        # Fetch weather data
        weather_info = get_weather(parsed_location['location'])
        
        # Generate the response
        response = chain.invoke({"user_input": user_input, "location": parsed_location['location'], "weather_info": weather_info})
        return response['text']

    return alfred_response

# Example usage
if __name__ == "__main__":
    alfred_chain = create_alfred_chain()
    print(alfred_chain("What should I wear in New York today?"))