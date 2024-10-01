from flask import Flask, request, jsonify
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
                                full_message += data["message"]["content"]

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
    return "Flask server is running. Please use POST /completion for API requests."

@app.route('/completion', methods=['POST'])
def generate_completion():
    # 사용자가 보낸 요청 데이터를 콘솔에 출력
    data = request.json
    print(f"사용자 요청 데이터: {data}")

    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiY44jeuohr7Mbc05w5ZuPul2cHopJKX0mgoeUHclkAq59',
        api_key_primary_val='7dwPwpWwd4nAycOnUJCKzU8PhIG19zSWZtC4TlSG',
        request_id='4baf4708-3413-47da-aa5d-a194f5b56ba3'
    )
    
    result = completion_executor.execute(data)

    # 처리 후 결과를 콘솔에 출력
    print(f"최종 결과: {result}")
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
