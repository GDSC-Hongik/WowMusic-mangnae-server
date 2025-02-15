from rest_framework import serializers
from .models import Song, Keyword


class KeywordSerializer(serializers.ModelSerializer):
    class Mete:
        model = Keyword
        fields = ['category','keyword']

class SongSerializer(serializers.ModelSerializer):
    keywords = KeywordSerializer(many=True)

    class Meta:
        model = Song
        fields = '__all__'