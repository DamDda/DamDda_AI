# Clova Studio Provided.

import requests

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

        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-003',
                           headers=headers, json=completion_request, stream=True) as r:
            for line in r.iter_lines():
                if line:
                    print(line.decode("utf-8"))


if __name__ == '__main__':
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiY44jeuohr7Mbc05w5ZuPul2cHopJKX0mgoeUHclkAq59',
        api_key_primary_val='7dwPwpWwd4nAycOnUJCKzU8PhIG19zSWZtC4TlSG',
        request_id='4baf4708-3413-47da-aa5d-a194f5b56ba3'
    )

    preset_text = [{"role":"system","content":"당신은 사용자가 입력한 정보를 바탕으로 크라우드펀딩 프로젝트의 상세 페이지를 생성하는 AI입니다.\n\n\n생성된 텍스트는 사용자가 제공한 정보를 충실히 반영하면서 일관성 있고 유창하게 작성되어야 합니다.\n\n\n사용자는 크라우드펀딩 프로젝트에 대한 구체적인 정보를 제공합니다:\n\n\n\"카테고리\"\n\"제목\"\n\"태그\" (5개)\n\"설명\"\n프로젝트 썸네일 이미지\n사용자가 상세 페이지에 넣고 싶은 관련 이미지\n입력된 정보를 바탕으로 명확하고 매력적인 언어로 상세 페이지를 작성하세요. 톤은 전문적이면서도 친근해야 합니다. 사용자가 제공한 정보와 이미지를 분석하여 고객의 구매를 유도할 수 있는 효과적인 마케팅 문구도 추가하세요.\n\n\n제품의 특징을 바탕으로, 고객이 구매 욕구를 느낄 수 있는 제품만의 장점 또는 특징을 파악하고, 각각의 특징에 대해 제목과 내용을 만들어 주세요. 제목과 내용의 구조는 다음과 같습니다:\n\n\n제목: 해당 특징을 설명하는 흥미로운 문구로 짧고 간결하게 작성하세요. 언어 유희나 영어를 적절히 섞어서 효과적인 마케팅 문구처럼 만들어 주세요.\n내용: 해당 특징의 제목에 맞는 설명을 짧고 간결하게 서술하세요. 구체적인 정보를 제공하되, 너무 길지 않도록 주의하세요.\n사용자가 제공하지 않은 정보나 불확실한 내용을 일반화하지 마세요. 반드시 프로젝트의 주제에 맞는 결과를 생성하세요."},{"role":"user","content":"카테고리: 기념품, 제목: 국립중앙박물관 콜라보 맥세이프 카드지갑, 태그: 전통, 기념품, 꽃, 카드지갑, 악세사리, 설명: 국립중앙박물관의 특정 작품을 카드지갑의 뒷쪽에 새긴 기념품입니다. 한국의 예술 작품에 대한 이해를 높이고 전통적인 멋을 느낄 수 있습니다. 프로젝트 썸네일 이미지: 없음, 프로젝트 관련 이미지: 없음."},{"role":"assistant","content":"**국립중앙박물관 콜라보 맥세이프 카드지갑**\n\n[전통, 기념품, 꽃, 카드지갑, 악세사리]\n\n국립중앙박물관의 아름다운 작품을 담은 맥세이프 카드지갑을 소개합니다.\n\n**한국의 전통적인 멋을 담은 카드지갑**\n\n국립중앙박물관의 특정 작품을 카드지갑의 뒷쪽에 새겨, 한국의 예술 작품에 대한 이해를 높이고 전통적인 멋을 느낄 수 있습니다.\n\n**맥세이프 호환**\n\n애플 맥세이프와 호환되어 아이폰에 쉽게 부착할 수 있으며, 카드지갑을 편리하게 사용할 수 있습니다.\n\n**간편한 카드 수납**\n\n카드지갑 내부에는 카드를 최대 2장까지 수납할 수 있으며, 카드를 쉽게 넣고 뺄 수 있어 편리합니다.\n\n**다양한 색상**\n\n다양한 색상으로 제공되어, 자신의 취향에 맞는 색상을 선택할 수 있습니다.\n\n**국립중앙박물관과의 콜라보**\n\n국립중앙박물관과의 콜라보로 제작된 제품으로, 국립중앙박물관의 작품을 일상에서 즐길 수 있습니다.\n\n**선물용으로도 추천**\n\n전통적인 멋과 현대적인 기능을 모두 갖춘 제품으로, 선물용으로도 추천합니다.\n\n국립중앙박물관의 작품을 담은 맥세이프 카드지갑으로, 일상에서 한국의 전통적인 멋을 즐겨보세요."}]

    request_data = {
        'messages': preset_text,
        'topP': 0.8,
        'topK': 0,
        'maxTokens': 523,
        'temperature': 0.5,
        'repeatPenalty': 1.5,
        'stopBefore': [],
        'includeAiFilters': True,
        'seed': 0
    }

    print(preset_text)
    completion_executor.execute(request_data)
