from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv

load_dotenv()
@tool
def get_weather(city: str) -> str: