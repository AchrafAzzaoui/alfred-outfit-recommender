from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, AgentType
from weather_tool import get_weather
from dotenv import load_dotenv
import os
from langchain.output_parsers import RegexParser

load_dotenv()

def create_alfred_chain():
    llm = ChatOpenAI(temperature=0.7)
    
    prompt = ChatPromptTemplate.from_template(
        "You are Alfred, Batman's butler. You're having a conversation with someone who is asking for "
        "outfit advice based on the weather in {location}. Use the get_weather tool to fetch "
        "current weather data, then provide an outfit recommendation in your characteristic style. "
        "Your response should include relevant weather information and specific clothing suggestions. "
        "Remember to maintain a formal, polite, and slightly witty tone throughout the conversation. "
        "If the user's input doesn't seem to be a location or a weather-related query, respond appropriately "
        "while gently steering the conversation back to outfit recommendations.\n\n"
        "User's input: {user_input}\n"
        "Weather data: {weather_info}\n"
        "Your response:"
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    agent = initialize_agent(
        [get_weather],
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    def alfred_response(user_input):
        # Use the LLM to parse the user input and extract the location
        parse_prompt = ChatPromptTemplate.from_template(
            "Extract the location from the following user input: {user_input}\n"
            "Location:"
        )
        parse_chain = LLMChain(llm=llm, prompt=parse_prompt)
        raw_location = parse_chain.run(user_input=user_input).strip()

        # Use an output parser to sanitize the parser LLM's generated response
        location_parser = RegexParser(regex=r"Location:\s*(.*)", output_keys=["location"])
        parsed_location = location_parser.parse(raw_location)
        location = parsed_location["location"]

        # Fetch the weather information using the extracted location
        weather_info = agent.run(f"Get the current weather in {location}")

        # Generate the outfit recommendation
        return chain.run(location=location, user_input=user_input, weather_info=weather_info)
    return alfred_response

if __name__ == "__main__":
    # Test the chain
    alfred = create_alfred_chain()
    print(alfred("What should I wear in New York today?"))