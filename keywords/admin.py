from django.contrib import admin
from .models import Keyword, Song, Song_Keyword

# Register your models here.
@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'category')

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'youtube_url')

@admin.register(Song_Keyword)
class Song_KeywordAdmin(admin.ModelAdmin):
    list_display = ('song', 'keyword')



