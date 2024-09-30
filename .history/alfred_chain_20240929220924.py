from langchain_community import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, AgentType
from langchain.output_parsers import RegexParser
from weather_tool import get_weather  # Assuming get_weather is defined in get_weather.py

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
    raw_location = parse_chain.invoke(user_input=user_input).strip()

    # Use an output parser to sanitize the parser LLM's generated response
    location_parser = RegexParser(regex=r"Location:\s*(.*)", output_keys=["location"])
    parsed_location = location_parser.parse(f"Location: {raw_location}")

    # Fetch weather data and generate response
    weather_info = get_weather(parsed_location['location'])
    response = chain.invoke(user_input=user_input, weather_info=weather_info)
    return response

# Example usage
if __name__ == "__main__":
    print(alfred_response("What should I wear in New York today?"))