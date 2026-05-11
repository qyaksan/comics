from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.core.paginator import Paginator
from .models import Comic, Review
from .forms import ReviewForm

def comic_list(request):
    comics = Comic.objects.all()
    # Фильтрация по жанру
    genre_filter = request.GET.get('genre')
    if genre_filter and genre_filter != '':
        comics = comics.filter(genre=genre_filter)
    # Поиск по названию
    search_q = request.GET.get('q')
    if search_q:
        comics = comics.filter(Q(title__icontains=search_q))
    # Сортировка
    sort_by = request.GET.get('sort')
    if sort_by == 'title':
        comics = comics.order_by('title')
    elif sort_by == '-title':
        comics = comics.order_by('-title')
    elif sort_by == 'release_date':
        comics = comics.order_by('release_date')
    elif sort_by == '-release_date':
        comics = comics.order_by('-release_date')
    elif sort_by == 'rating':
        comics = comics.annotate(avg_rating=Avg('reviews__rating')).order_by('avg_rating')
    elif sort_by == '-rating':
        comics = comics.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    else:
        comics = comics.order_by('-created_at')
    # Пагинация
    paginator = Paginator(comics, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'genres': Comic.GENRE_CHOICES,
        'current_genre': genre_filter,
        'current_sort': sort_by,
        'search_q': search_q,
    }
    return render(request, 'comics/comic_list.html', context)

def comic_detail(request, pk):
    comic = get_object_or_404(Comic, pk=pk)
    reviews = comic.reviews.all().order_by('-created_at')
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.comic = comic
            review.save()
            return redirect('comic_detail', pk=comic.pk)
    else:
        form = ReviewForm()
    context = {
        'comic': comic,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'comics/comic_detail.html', context)

@login_required
def edit_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('comic_detail', pk=review.comic.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'comics/add_review.html', {'form': form})