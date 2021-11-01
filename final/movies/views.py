from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe, require_POST, require_http_methods
from .models import Movie
from .forms import MovieForm
from django.http.response import HttpResponse
from django.http import JsonResponse

from django.core.paginator import Paginator

@require_safe
def index(request):
    # movies.json을 db에 저장하고, db에있는 영화 가져오기
    movies = Movie.objects.all()

    paginator = Paginator(movies, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'posts': posts
    }
    return render(request, 'movies/index.html', context)


@require_safe
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.review_set.all()

    # tmdb의 10점 만점 기준의 점수를
    # 100점 기준으로 환산해서 소수점 없애기
    percentage = int(movie.vote_average * 10)

    context = {
        'movie': movie,
        'reviews': reviews,
        'percentage': percentage,
    }
    return render(request, 'movies/detail.html', context)


@require_http_methods(['GET', 'POST'])
def update(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance = movie)
        if form.is_valid():
            form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm(instance = movie)

    context = {
        'form':form,
        'movie':movie
    }
    return render(request, 'movies/update.html', context)


@require_POST
def delete(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie.delete()
    return redirect('movies:index')


@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()          
            return redirect('movies:detail', movie.pk)
    else: 
        form = MovieForm()
    
    context = {
        'form': form,
    }
    return render(request, 'movies/create.html', context)
    

@require_POST
def like(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        user = request.user

        if movie.like_users.filter(pk=user.pk).exists():
            movie.like_users.remove(user)
            liked = False
        else:
            movie.like_users.add(user)
            liked = True
            
        context = {
            'liked': liked,
            'count': movie.like_users.count(),
        }
        return JsonResponse(context)
    return HttpResponse(status=401)