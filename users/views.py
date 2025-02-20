from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer


# Create your views here.
def home_view(request):
    return render(request, "home.html")

@api_view(['POST'])
def login_view(request):
    if request.method == "POST":
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username = email, password = password)
        if user is not None:
            print("인증 성공!")
            login(request, user)
            return Response({"message": f"{user.username}님 환영합니다!", 
                             "username" : user.username,
                             "email" : user.email,
                             "redirect_url":"home/"}, status = 200)
        else:
            print("인증 실패!")
    return Response({"error": "존재하지 않는 회원입니다.", "redirect_url":"login/"}, status=401)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({"message" : "로그아웃되었습니다."}, status=200)



@api_view(['POST'])
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

        return Response({"message" : f"{user.username}님 가입을 환영합니다. 로그인 화면으로 돌아갑니다."}, status =200)
        
        
    return Response({"error" : "올바르지 않은 정보입니다"}, status =402)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_view(request):
    if not request.user.is_authenticated:
        return Response({"error": "로그인이 필요합니다."}, status=401)
    
    user = request.user

    username = request.data.get("username", user.username)
    email = request.data.get("email", user.email)
    birth = request.data.get("birth", user.birth)


    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return Response({"error": "이미 사용 중인 이메일입니다."}, status=status.HTTP_409_CONFLICT)

    # 필드 값 업데이트
    user.username = username
    user.email = email
    user.birth = birth
    user.save()

    # 업데이트된 사용자 정보 반환
    return Response({
        "message": "회원 정보가 성공적으로 수정되었습니다.",
        "updated_user": {
            "username": user.username,
            "email": user.email,
            "birth": user.birth.strftime("%Y-%m-%d")  # 날짜를 문자열로 변환
        }
    }, status=status.HTTP_200_OK)