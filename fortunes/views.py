import openai
import os
from dotenv import load_dotenv
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


load_dotenv()  # .env 파일 로드
openai.api_key = os.getenv("OPENAI_API_KEY")  # 환경변수에서 API 키 읽기

def get_fortune(birthdate):
    # 예시로 생년월일에 맞는 운세를 ChatGPT API로 요청
    prompt = f"생년월일 {birthdate}에 맞는 운세를 알려줘."

    response = openai.Completion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=150
    )

    return response['choices'][0]['text'].strip()

@api_view(['GET'])
def fortune_view(request):
    birthdate = request.GET.get("birthdate", "")  # 쿼리 파라미터로 생년월일 받기

    if not birthdate:
        return Response({"error": "생년월일을 입력해주세요."}, status=400)

    # ChatGPT API 호출
    fortune = get_fortune(birthdate)

    return Response({"birthdate": birthdate, "fortune": fortune})
