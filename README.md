# Streaming chatbot with OpenAI functions

This chatbot utilizes OpenAI's function calling feature to invoke appropriate functions based on user input and stream the response back.

On top of the standard chat interface, the UI exposes the particular function called along with its arguments, as well as the response from the function.

**The current configuration defines two OpenAI functions that can be called**:
- `get_current_weather`: returns the current weather for a given location. Example input: `What's the weather like in New York?`
  - Note that the API returns temperature in Celsius by default. The time zone is set for Europe/Berlin, but this can be changed in `openai_functions.py`

- `get_search_results`: A langchain agent that uses SERP API as a tool to search the web. Example input: `Search the web for the best restaurants in Berlin`

from langchain.agents import initialize_agent, AgentType, Tool
from langchain import SerpAPIWrapper
from langchain.chat_models import ChatOpenAI
import requests
import json
import os


class OpenAIFunctions:
    @staticmethod
    def get_current_weather(longitude, latitude):
        """Get the current weather for a location"""
        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": "true",
                "timezone": "Europe/Berlin",
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return json.dumps(data["current_weather"])
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        return json.dumps({"error": "Failed to get weather"})

    @staticmethod
    def get_search_results(query):
        """Get search results for a query"""
        try:
            llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
            search = SerpAPIWrapper(
                serpapi_api_key=os.getenv("SERPAPI_API_KEY"),
            )
            tools = [
                Tool(
                    name="Search",
                    func=search.run,
                    description="useful for when you need to answer questions about current events. You should ask targeted questions",
                )
            ]
            agent = initialize_agent(
                tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True
            )
            res = agent.run(query)
            return json.dumps(res)
        except Exception as e:
            print(f"Error getting search results: {e}")
            return json.dumps({"error": "Failed to get search results"})
        
    @staticmethod
    def search_images(query, max_results=10):
        """Search for images using the SERPAPI image search service"""
        try:
            # Initialize SERPAPI client with your API key
            serpapi_api_key = os.getenv("SERPAPI_API_KEY")
            search = SerpAPIWrapper(serpapi_api_key=serpapi_api_key)

            # Define the parameters for the image search
            params = {
                "q": query,
                "tbm": "isch",  # Image search
                "num": max_results,  # Number of results to retrieve
            }

            # Perform the image search
            response = search.run(params)

            return json.dumps(response)
        except Exception as e:
            print(f"Error searching images: {e}")
            return json.dumps({"error": "Failed to search for images"})


FUNCTIONS_MAPPING = {
    "get_search_results": OpenAIFunctions.get_search_results,
    "get_current_weather": OpenAIFunctions.get_current_weather,
    "search_images": OpenAIFunctions.search_images,
}
