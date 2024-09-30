# Response Console Print Test.

import requests
import json


class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }

        full_message = ""
        ai_filter_data = []

        try:
            # 타임아웃 설정 (예: 30초)
            with requests.post(self._host + '/testapp/v1/chat-completions/HCX-003',
                               headers=headers, json=completion_request, stream=True, timeout=30) as r:
                for line in r.iter_lines():
                    if line:
                        decoded_line = line.decode("utf-8").strip()

                        # JSON으로 시작되지 않는 경우 건너뜀
                        if not decoded_line.startswith("data:"):
                            continue

                        try:
                            # "data:"를 제거한 부분을 JSON으로 파싱
                            json_data = decoded_line.split("data:")[-1].strip()

                            # 비어있는 데이터 확인
                            if not json_data:
                                continue

                            data = json.loads(json_data)

                            # 완전한 메시지 데이터를 수집
                            if "message" in data and data["message"]["role"] == "assistant":
                                full_message += data["message"]["content"]

                            # AI 필터 데이터를 누적해서 수집
                            if "aiFilter" in data:
                                ai_filter_data.extend(data["aiFilter"])

                        except json.JSONDecodeError:
                            print(f"JSON 디코딩 실패: {decoded_line}")
                            continue

        except requests.exceptions.Timeout:
            print("요청이 시간 내에 완료되지 않았습니다.")
        except requests.exceptions.RequestException as e:
            print(f"요청 중 오류 발생: {e}")

        # 이스케이프 문자가 해석된 상태로 출력
        print("=== 완성된 메시지 ===")
        print(full_message)  # 이스케이프 문자가 실제로 해석된 상태로 출력

        # AI 필터 정보도 함께 출력 (JSON 포맷)
        if ai_filter_data:
            print("\n=== AI 필터 정보 ===")
            print(json.dumps(ai_filter_data, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    # 직접 하드코딩된 값들
    category = "기념품"
    title = "국립중앙박물관 콜라보 맥세이프 카드지갑"
    tags = "전통, 기념품, 꽃, 카드지갑, 악세사리"
    description = "국립중앙박물관의 특정 작품을 카드지갑의 뒷쪽에 새긴 기념품입니다. 한국의 예술 작품에 대한 이해를 높이고 전통적인 멋을 느낄 수 있습니다."

    # 태그 리스트로 변환
    tags_list = [tag.strip() for tag in tags.split(",")]

    # 프롬프트에 하드코딩된 값 반영
    prompt = [
        {
            "role": "system",
            "content": f"""당신은 사용자가 입력한 정보를 바탕으로 크라우드펀딩 프로젝트의 상세 페이지를 생성하는 AI입니다.
            생성된 텍스트는 사용자가 제공한 정보를 충실히 반영하면서 일관성 있고 유창하게 작성되어야 합니다.
            사용자는 크라우드펀딩 프로젝트에 대한 구체적인 정보를 제공합니다:
            
            '카테고리': {category}
            '제목': {title}
            '태그': {', '.join(tags_list)}
            '설명': {description}
            
            프로젝트 썸네일 이미지: 없음
            프로젝트 관련 이미지: 없음
            
            입력된 정보를 바탕으로 명확하고 매력적인 언어로 상세 페이지를 작성하세요. 톤은 전문적이면서도 친근해야 합니다.
            사용자가 제공한 정보와 이미지를 분석하여 고객의 구매를 유도할 수 있는 효과적인 마케팅 문구도 추가하세요."""
        }
    ]

    # 요청 데이터 구성
    request_data = {
        'messages': prompt,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 523,
        'temperature': 0.5,
        'repeatPenalty': 1.5,
        'stopBefore': [],
        'includeAiFilters': True,
        'seed': 0
    }

    # CompletionExecutor 인스턴스 생성 및 실행
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiY44jeuohr7Mbc05w5ZuPul2cHopJKX0mgoeUHclkAq59',
        api_key_primary_val='7dwPwpWwd4nAycOnUJCKzU8PhIG19zSWZtC4TlSG',
        request_id='4baf4708-3413-47da-aa5d-a194f5b56ba3'
    )

    # 생성된 프롬프트 출력 및 실행
    completion_executor.execute(request_data)
