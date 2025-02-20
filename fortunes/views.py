from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import openai
import os

# Create your views here.

#openai.api_key = os.getenv("OPENAI_API_KEY")

#@api_view(['POST'])
#def get_fortune(request):
 #   try:
  #      birth_date = request.data.get("birth_date")
#
 #   if not birth_date:
  #      return Response({"error":"오잉"}, status=402)