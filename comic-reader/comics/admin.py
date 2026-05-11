from django.contrib import admin
from .models import Comic, Review, UserSettings

@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'release_date', 'created_at')
    search_fields = ('title',)
    list_filter = ('genre',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'comic', 'rating', 'created_at')
    list_filter = ('rating',)

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'font_size')