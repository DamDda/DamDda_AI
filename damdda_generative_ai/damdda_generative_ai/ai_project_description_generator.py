from flask import Flask, request, jsonify, Response
import requests
import json

app = Flask(__name__)

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

                        if not decoded_line.startswith("data:"):
                            continue

                        try:
                            json_data = decoded_line.split("data:")[-1].strip()

                            if not json_data:
                                continue

                            data = json.loads(json_data)

                            # 콘솔에 API에서 받은 데이터를 출력
                            print(f"API 응답 데이터: {data}")

                            if "message" in data and data["message"]["role"] == "assistant":
                                new_message = data["message"]["content"]

                                # 중복 방지를 위해 full_message에 추가된 메시지인지 확인
                                if new_message not in full_message:
                                    full_message += new_message

                            if "aiFilter" in data:
                                ai_filter_data.extend(data["aiFilter"])

                        except json.JSONDecodeError:
                            print(f"JSON 디코딩 실패: {decoded_line}")
                            continue

        except requests.exceptions.Timeout:
            print("요청이 시간 내에 완료되지 않았습니다.")
        except requests.exceptions.RequestException as e:
            print(f"요청 중 오류 발생: {e}")

        return {
            "full_message": full_message,
            "ai_filter_data": ai_filter_data
        }

# GET 요청을 위한 간단한 상태 확인 엔드포인트 추가
@app.route('/', methods=['GET'])
def home():
    return "Flask server is running. Invalid access. Please try again."

@app.route('/api/generative-ai/project-description', methods=['POST'])
def generate_completion():
    # 사용자가 보낸 요청 데이터를 콘솔에 출력
    data = request.json
    print(f"사용자 요청 데이터: {data}")

    # 카테고리, 제목, 태그, 설명 추출
    category = data.get("category", "")
    title = data.get("title", "")
    tags = data.get("tags", [])
    description = data.get("description", "")

    # 태그 리스트를 문자열로 변환
    tags_list = [tag.strip() for tag in tags]

    # 최적화된 프롬프트 구성
    prompt = [
        {
            "role": "system",
            "content": f"""다음 정보를 바탕으로 크라우드펀딩 프로젝트 상세 페이지를 작성하세요:
            제목: {title}
            카테고리: {category}
            태그: {', '.join(tags_list)}
            설명: {description}
            톤은 전문적이면서도 친근해야 하며, 고객의 관심을 끌 수 있는 마케팅 문구를 포함하세요."""
        }
    ]

    # API 요청 데이터 구성
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

    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiY44jeuohr7Mbc05w5ZuPul2cHopJKX0mgoeUHclkAq59',
        api_key_primary_val='7dwPwpWwd4nAycOnUJCKzU8PhIG19zSWZtC4TlSG',
        request_id='4baf4708-3413-47da-aa5d-a194f5b56ba3'
    )
    
    result = completion_executor.execute(request_data)

    # 처리 후 결과를 콘솔에 출력
    print(f"최종 결과: {result}")

    # full_message에서 문제될 수 있는 줄바꿈이나 특수 문자 이스케이프 처리
    full_message = result["full_message"].replace("\n", "\\n").replace("\t", "\\t")

    try:
        # 유니코드 이스케이프 해제
        result['full_message'] = json.loads(f'"{full_message}"')
    except json.JSONDecodeError as e:
        print(f"JSON 디코딩 실패: {e}")
        result['full_message'] = full_message  # 디코딩이 실패하면 그대로 유지

    # UTF-8로 인코딩된 응답 반환
    response = Response(
        response=json.dumps(result, ensure_ascii=False),  # ensure_ascii=False로 한글 유니코드 방지
        content_type='application/json; charset=utf-8'
    )
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
