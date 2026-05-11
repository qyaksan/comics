# comics/context_processors.py
from comics.models import UserSettings   # вместо users.models

def theme_settings(request):
    if request.user.is_authenticated:
        settings, _ = UserSettings.objects.get_or_create(user=request.user)
        theme = settings.theme
        font_size = settings.font_size
    else:
        theme = request.COOKIES.get('theme', 'light')
        font_size = request.COOKIES.get('font_size', 'medium')
    return {
        'user_theme': theme,
        'user_font_size': font_size,
    }