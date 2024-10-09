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
            "content": """
            제공된 정보를 바탕으로, 크라우드 펀딩 프로젝트의 주요 기능, 혜택, 특징을 소개하는 여러 개의 마케팅 문구와 그에 대한 간단한 설명을 작성하세요. 각 문구는 후원자들의 관심을 끌 수 있도록 설득력 있게 구성하고, 설명은 간결하면서도 정확하게 프로젝트의 특성을 전달하세요. 마케팅 문구는 **굵게**, 설명은 _기울임체_로 표시되도록 하세요. 불필요한 멘트는 생략하고, 자연스럽게 이어지는 구조로 작성하세요.

            제공된 정보:
            제목: {title}
            카테고리: {category}
            태그: {', '.join(tags_list)}
            설명: {description}

            결과 형식:
            **굵은 마케팅 문구**
            _간결한 설명_

            참고 사항: 후원자들이 이 프로젝트가 크라우드 펀딩임을 인지하고, 그들의 참여가 중요한 이유를 자연스럽게 강조하세요.
            """
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
