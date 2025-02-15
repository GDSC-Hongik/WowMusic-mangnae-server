from django.db import models

# Create your models here.

class Keyword(models.Model):
    EMOTION = 'emotion'
    WEATHER = 'weather'
    SITUATION = 'situation'
    GENRE = 'genre'

    CATEGORY = [
        (EMOTION, 'Emotion'),
        (WEATHER, 'Weather'),
        (SITUATION, 'Situation'),
        (GENRE, 'Genre')
    ]
    
    keyword = models.CharField(max_length=10, unique=True, default = "")
    category = models.CharField(max_length=10, choices=CATEGORY, default=EMOTION)
    
    def __str__(self):
        return f"{self.keyword} ({self.category})"


class Song(models.Model):
    title = models.CharField(max_length=20)
    artist = models.CharField(max_length=20)
    youtube_url = models.URLField(unique=True, null=True, default="")
    
    keywords = models.ManyToManyField(Keyword, through='Song_Keyword')
    def __str__(self):
        return f"{self.title} - {self.artist}"
    

class Song_Keyword(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)

    class Meta:
        db_table = 'keywords_song_keyword'

    def __str__(self):
        return f"{self.song} - {self.keyword}"