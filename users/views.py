from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

import jwt
from django.conf import settings
from datetime import datetime, timedelta, timezone



# Create your views here.
def decode_jwt_token(token):
    try:
        # JWT 토큰을 디코딩하여 유효한지 확인
        decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        # 토큰 만료 에러 처리
        return {'error': '토큰이 만료되었습니다.'}
    except jwt.InvalidTokenError:
        # 유효하지 않은 토큰 에러 처리
        return {'error': '유효하지 않은 토큰입니다.'}

@api_view(['POST'])
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username = email, password = password)
        
        if user is not None:
            # JWT 토큰 생성
            expiration_time = datetime.now(timezone.utc) + timedelta(hours=1)  # 만료 시간 설정
            payload = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'exp': expiration_time
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            return Response({
                "message": f"{user.username}님 환영합니다!",
                "redirect_url": "home/",
                "token": token  # 생성된 토큰을 응답에 포함
            }, status=200)
        else:
            return Response({"error": "존재하지 않는 회원입니다.", "redirect_url": "login/"}, status=401)
        pass


@api_view(['POST'])
def logout_view(request):
    return Response({"message" : "로그아웃되었습니다. 클라이언트에서 토큰을 삭제해주세요."}, status=200)



@api_view(['POST'])
@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        birth = request.data.get('birth')

        if not all([username, email, password, birth]):
            return Response({"error": "모든 필드를 입력해주세요."}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.birth = birth
        user.save()

        # JWT 토큰 생성
        expiration_time = datetime.now(timezone.utc) + timedelta(hours=1)  # 만료 시간 설정
        payload = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'exp': expiration_time
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return Response({"message" : f"{user.username}님 가입을 환영합니다. 로그인 화면으로 돌아갑니다.", 
                         "token": token }, status =200)
        
        
    return Response({"error" : "올바르지 않은 정보입니다"}, status =402)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_view(request):
    
    user = request.user

    username = request.data.get("username", user.username)
    email = request.data.get("email", user.email)
    password = request.data.get("password", user.password)

    # 필드 값 업데이트
    user.username = username
    user.email = email
    user.password = password
    user.save()

    # 업데이트된 사용자 정보 반환
    return Response({
        "message": "회원 정보가 성공적으로 수정되었습니다.",
        "updated_user": {
            "username": user.username,
            "email": user.email,
            "birth": user.password
        }
    }, status=status.HTTP_200_OK)

