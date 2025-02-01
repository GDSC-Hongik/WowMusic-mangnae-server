from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from rest_framework.decorators import api_view
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
        user = authenticate(email = email, password = password)
        if user is not None:
            print("인증 성공!")
            login(request, user)
            return Response({"message": f"{user.username}님 환영합니다!", "redirect_url":"home/"}, status = 200)
        else:
            print("인증 실패!")
    return Response({"error": "존재하지 않는 회원입니다.", "redirect_url":"login/"}, status=405)


@api_view(['GET'])
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

        user = User.objects.create_user(username=username, email=email, password=password)
        user.birth = birth
        user.save()

        return Response({"message" : f"{user.username}님 가입을 환영합니다. 로그인 화면으로 돌아갑니다."}, status =200)
        
    return Response({"error" : "올바르지 않은 정보입니다"}, status =405)

