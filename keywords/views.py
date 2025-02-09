from .models import Keyword, Song, SongKeyword
from .serializers import SongSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count


# Create your views here.
@api_view(['GET'])
def get_song_view(request):

    keywords = request.GET.getlist('keywords')
    keyword_objects = Keyword.objects.filter(keyword__in=keywords)

    if not keyword_objects:
        return Response({'message': 'One or more keywords not found!'}, status=404)
    

    songs_with_keyword = Song.objects.filter(keywords__in=keyword_objects).distinct() #중복 노래 제외

    most_related_song = songs_with_keyword.annotate(keyword_count=Count('keywords')).order_by('-keyword_count').first()


    if most_related_song:
        song_data = {
            "title": most_related_song.title,
            "artist": most_related_song.artist,
            "keywords": [
                {keyword.category: keyword.keyword} for keyword in most_related_song.keywords.all()
            ]
        }
        return Response(song_data)
    
    else:
        return Response({'message':'이게무슨오류일까요...'}, status=404)