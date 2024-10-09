def generate_prompt(title: str, category: str, tags_list: list, description: str) -> list:
    """
    Generate a prompt for the generative AI based on the given crowdfunding project details.
    
    Args:
        title (str): The project title.
        category (str): The category of the project.
        tags_list (list): A list of tags for the project.
        description (str): The detailed project description.
    
    Returns:
        list: A list containing the prompt for the AI model.
    """
    
    prompt = [
        {
            "role": "system",
            "content": """다음 정보를 바탕으로 '상세 설명' 섹션만 작성하세요:
            제목: {title}
            카테고리: {category}
            태그: {', '.join(tags_list)}
            설명: {description}
            
            상세 설명만 작성하세요. 상세 설명에서는 프로젝트의 구체적인 기능, 혜택, 특징 등을 전문적이면서도 친근한 톤으로 작성하세요. 고객의 관심을 끌 수 있는 마케팅 문구를 포함하세요."""
        }
    ]

    return prompt
    

def prepare_request_data(prompt: list) -> dict:
    """
    Prepare the necessary data for the API request using the generated prompt.
    
    Args:
        prompt (list): A list containing the AI prompt.
    
    Returns:
        dict: The data structure containing the API request parameters.
    """
    
    request_data = {
        'messages': prompt,
        'topP': 0.8,  # Controls nucleus sampling (higher = more diverse responses)
        'topK': 0,    # Controls top-K sampling (0 = disabled)
        'maxTokens': 523,  # Maximum number of tokens the model can return
        'temperature': 0.5,  # Controls randomness in the response (0 = deterministic)
        'repeatPenalty': 1.5,  # Penalty for repeating tokens
        'stopBefore': [],  # No specific stopping conditions
        'includeAiFilters': True,  # Whether to include AI filter data
        'seed': 0  # Use a fixed seed for reproducibility
    }
    return request_data
