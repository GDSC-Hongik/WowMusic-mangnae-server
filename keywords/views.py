from django.shortcuts import render
from .models import Keyword, Song, Song_Keyword
from .serializers import SongSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count


# Create your views here.
@api_view(['GET'])
def get_song_view(request):

    selected_keywords = request.GET.getlist('keywords')

    keyword_objects = Keyword.objects.filter(keyword__in=selected_keywords)

    if not keyword_objects:
        return Response({'message': 'One or more keywords not found!'}, status=404)
    

    songs_with_keyword = Song.objects.filter(song_keyword__keyword__keyword__in=keyword_objects).distinct() #중복 노래 제외

    recommended_song = songs_with_keyword.annotate(
        match_count = Count('song_keywords')
    ).order_by('-match_count').first()

    if recommended_song:
        song_data = {
            "title": recommended_song.title,
            "artist": recommended_song.artist,
            "keywords": [
                {keyword.category: keyword.keyword} for keyword in recommended_song.keywords.all()
            ]
        }
        return Response(song_data)
    
    else:
        return Response({'message':'이게무슨오류일까요...'}, status=404)