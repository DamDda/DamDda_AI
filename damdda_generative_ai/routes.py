from flask import Blueprint, request, jsonify, Response
from .executor import CompletionExecutor
from .config import Config
from .prompt_generator import generate_prompt, prepare_request_data
import json

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def home():
    # Basic route to check if the server is running
    return "Flask server is running. Invalid access. Please try again."

@main_bp.route('/api/generative-ai/project-description', methods=['POST'])
def generate_completion():
    # Parse JSON data from the incoming POST request
    data = request.json
    print(f"사용자 요청 데이터: {data}")

    # Extract necessary fields from the request payload
    category = data.get("category", "")
    title = data.get("title", "")
    tags = data.get("tags", [])
    description = data.get("description", "")

    # Clean up tags by removing excess whitespace
    tags_list = [tag.strip() for tag in tags]
    
    # Create the AI prompt based on input data
    prompt = generate_prompt(title, category, tags_list, description)

    # Structure the request data for the API call
    request_data = prepare_request_data(prompt)

    # Initialize the completion executor with API configuration
    completion_executor = CompletionExecutor(
        host=Config.HOST,
        api_key=Config.API_KEY,
        api_key_primary_val=Config.API_KEY_PRIMARY_VAL,
        request_id=Config.REQUEST_ID
    )

    # Execute the API call and retrieve the result
    result = completion_executor.execute(request_data)

    # Format the AI-generated message by escaping certain characters
    full_message = result["full_message"].replace("\n", "\\n").replace("\t", "\\t")

    try:
        # Attempt to decode the formatted message into a proper JSON object
        result['full_message'] = json.loads(f'"{full_message}"')
    except json.JSONDecodeError as e:
        print(f"JSON 디코딩 실패: {e}")
        result['full_message'] = full_message  # Fallback to raw message if decoding fails

    # Return the processed result as a JSON response to the client
    response = Response(
        response=json.dumps(result, ensure_ascii=False),  # Prevent Unicode escaping
        content_type='application/json; charset=utf-8'
    )
    return response
