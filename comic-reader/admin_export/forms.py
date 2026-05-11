from django import forms
from comics.models import Comic, Review, UserSettings
from django.contrib.auth.models import User

class ExportForm(forms.Form):
    MODEL_CHOICES = [
        ('comic', 'Комиксы'),
        ('review', 'Отзывы'),
        ('user', 'Пользователи'),
        ('usersettings', 'Настройки пользователей'),
    ]

    tables = forms.MultipleChoiceField(
        choices=MODEL_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Таблицы для экспорта'
    )
    fields_comic = forms.MultipleChoiceField(
        choices=[(f.name, f.verbose_name) for f in Comic._meta.fields if f.name not in ('created_at', 'updated_at')],
        required=False,
        label='Поля комиксов'
    )
    fields_review = forms.MultipleChoiceField(
        choices=[(f.name, f.verbose_name) for f in Review._meta.fields if f.name not in ('created_at', 'updated_at')],
        required=False,
        label='Поля отзывов'
    )
    fields_user = forms.MultipleChoiceField(
        choices=[('id', 'ID'), ('username', 'Логин'), ('email', 'Email'), ('is_staff', 'Администратор')],
        required=False,
        label='Поля пользователей'
    )
    fields_usersettings = forms.MultipleChoiceField(
        choices=[(f.name, f.verbose_name) for f in UserSettings._meta.fields if f.name not in ('created_at', 'updated_at', 'user')],
        required=False,
        label='Поля настроек'
    )