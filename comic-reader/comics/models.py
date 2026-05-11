from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Comic(BaseModel):
    GENRE_CHOICES = [
        ('superhero', 'Супергероика'),
        ('manga', 'Манга'),
        ('horror', 'Ужасы'),
        ('fantasy', 'Фэнтези'),
        ('sci-fi', 'Научная фантастика'),
        ('other', 'Другое'),
    ]

    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    cover = models.ImageField(upload_to='comic_covers/', blank=True, null=True, verbose_name='Обложка')
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='other', verbose_name='Жанр')
    release_date = models.DateField(verbose_name='Дата выпуска')

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(r.rating for r in reviews) / len(reviews)
        return 0

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Комикс'
        verbose_name_plural = 'Комиксы'
        ordering = ['-created_at']

class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='Пользователь')
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name='reviews', verbose_name='Комикс')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Оценка')
    comment = models.TextField(verbose_name='Комментарий', blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.comic.title} ({self.rating})'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('user', 'comic')  # один пользователь – один отзыв на комикс

class UserSettings(BaseModel):
    THEME_CHOICES = [
        ('light', 'Светлая'),
        ('dark', 'Тёмная'),
    ]
    FONT_SIZE_CHOICES = [
        ('small', 'Маленький'),
        ('medium', 'Средний'),
        ('large', 'Большой'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings', verbose_name='Пользователь')
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light', verbose_name='Тема')
    font_size = models.CharField(max_length=10, choices=FONT_SIZE_CHOICES, default='medium', verbose_name='Размер шрифта')

    def __str__(self):
        return f'Настройки {self.user.username}'