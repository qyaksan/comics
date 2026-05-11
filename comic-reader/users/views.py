from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserSettingsForm
from comics.models import UserSettings

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Создаём настройки по умолчанию
            UserSettings.objects.create(user=user)
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def user_settings(request):
    settings, _ = UserSettings.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('user_settings')
    else:
        form = UserSettingsForm(instance=settings)
    return render(request, 'users/settings.html', {'form': form})