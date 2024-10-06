import requests
import json
from .config import Config  # Import the configuration class for API settings

class CompletionExecutor:
    def __init__(self):
        # Initialize the required configurations from the config class
        self._host = Config.HOST
        self._api_key = Config.API_KEY
        self._api_key_primary_val = Config.API_KEY_PRIMARY_VAL
        self._request_id = Config.REQUEST_ID

    def execute(self, completion_request):
        # Set the headers needed for the API request
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,  # API key for authentication
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,  # API Gateway key
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,  # Request ID for tracking
            'Content-Type': 'application/json; charset=utf-8',  # Content type
            'Accept': 'text/event-stream'  # Accept server-sent events (SSE)
        }

        full_message = ""  # Store the complete response message
        ai_filter_data = []  # Store any AI filter-related data

        try:
            # Send a POST request to the API with the provided completion_request data
            with requests.post(self._host + '/testapp/v1/chat-completions/HCX-003',
                               headers=headers, json=completion_request, stream=True, timeout=30) as r:
                # Process the streamed response line by line
                for line in r.iter_lines():
                    if line:
                        decoded_line = line.decode("utf-8").strip()

                        # Ensure we're processing valid data lines
                        if not decoded_line.startswith("data:"):
                            continue

                        try:
                            # Extract and load JSON from the event stream
                            json_data = decoded_line.split("data:")[-1].strip()

                            if not json_data:
                                continue

                            data = json.loads(json_data)
                            print(f"API response data: {data}")  # Debugging: log API response

                            # Append new message content if it's from the assistant
                            if "message" in data and data["message"]["role"] == "assistant":
                                new_message = data["message"]["content"]

                                # Ensure no duplication of the message
                                if new_message not in full_message:
                                    full_message += new_message

                            # Collect AI filter data if present
                            if "aiFilter" in data:
                                ai_filter_data.extend(data["aiFilter"])

                        except json.JSONDecodeError:
                            print(f"Failed to decode JSON: {decoded_line}")  # Handle JSON parsing errors
                            continue

        except requests.exceptions.Timeout:
            print("The request did not complete within the time limit.")  # Handle request timeout
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the request: {e}")  # Handle any other request-related errors

        # Return the full message and any AI filter data collected from the API
        return {
            "full_message": full_message,
            "ai_filter_data": ai_filter_data
        }
