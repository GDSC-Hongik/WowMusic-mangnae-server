from .models import Keyword, Song, Song_Keyword
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count, Q
from random import randint


@api_view(['GET'])
def get_song_view(request):
    selected_keywords = [request.GET[key] for key in request.GET if key.startswith('keyword')]
    selected_categories = [request.GET[key] for key in request.GET if key.startswith('category')]

    keyword_objects = Keyword.objects.filter(keyword__in=selected_keywords)
    if selected_categories:
        keyword_objects = keyword_objects.filter(category__in=selected_categories)

    recommended_songs = []

    if not keyword_objects.exists():
        total_songs = Song.objects.count()
        if total_songs >= 5:
            random_offset = randint(0, total_songs - 5)
            recommended_songs = list(Song.objects.all()[random_offset:random_offset + 5])
        else:
            recommended_songs = list(Song.objects.all())

    else:
        song_ids = Song.objects.filter(song_keyword__keyword__in=keyword_objects).distinct().values_list('id', flat=True)
        songs_with_keyword = Song.objects.filter(id__in=song_ids)

        songs_with_match_count = songs_with_keyword.annotate(
            match_count=Count('song_keyword', filter=Q(song_keyword__keyword__in=keyword_objects), distinct=True)
        ).order_by('-match_count')

        # 매칭 안 된 곡들 중에서 랜덤 5곡 선택
        songs_with_zero_match_count = Song.objects.exclude(id__in=song_ids).order_by('?')[:max(0, 5 - len(songs_with_match_count))]

        recommended_songs = list(songs_with_match_count) + list(songs_with_zero_match_count)

        if len(recommended_songs) < 5:
            total_remaining_songs = Song.objects.exclude(id__in=[song.id for song in recommended_songs]).count()
            if total_remaining_songs > 0:
                random_offset = randint(0, total_remaining_songs - (5 - len(recommended_songs)))
                remaining_songs = Song.objects.exclude(id__in=[song.id for song in recommended_songs])[random_offset:random_offset + (5 - len(recommended_songs))]
                recommended_songs.extend(remaining_songs)

    song_data = [
        {
            "title": song.title,
            "artist": song.artist,
            "youtube_url": song.youtube_url,
            "keywords": [{keyword.category: keyword.keyword} for keyword in song.keywords.all()],
            "match_count": getattr(song, 'match_count', 0)  # match_count가 없는 경우 0으로 처리
        }
        for song in recommended_songs
    ]

    return Response(song_data if song_data else {'message': '추천할 곡이 없습니다'}, status=200)
