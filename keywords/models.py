from django.db import models

# Create your models here.

class Keyword(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=20)
    artist = models.CharField(max_length=20)
    keywords = models.ManyToManyField(Keyword, related_name="songs")

    def __str__(self):
        return self.name
    

class SongKeyword(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.song.title} - {self.keyword.name}"