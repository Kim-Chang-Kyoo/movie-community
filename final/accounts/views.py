from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from .forms import CustomUserCreationForm, CustomUserChangeForm

import requests
from django.core.paginator import Paginator

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('main:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('main:index')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('main:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'main:index')
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    auth_logout(request)
    return redirect('main:index')


@login_required
def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)


@require_POST
def follow(request, user_pk):
    person = get_object_or_404(get_user_model(), pk=user_pk)
    
    if request.user.is_authenticated:
        user = request.user
        if person != user:
            if person.followers.filter(pk=user.pk).exists():
                person.followers.remove(user)
                followed = False
            else:
                person.followers.add(user)
                followed = True
        
        context = {
            'followed' : followed,
            'count' : person.followers.count()
        }
        return JsonResponse(context)

    return redirect('accounts:profile', person.username)

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('main:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        # form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('main:index')
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)



@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect('main:index')



@login_required
def recommended(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    random_movies = person.like_movies.all().order_by('?')
    
    # 좋아요한 영화가 있을 때
    if random_movies:
        random_movie = random_movies[0]

        api_key = '55ef856f2894b48b09a2d30c1fbc3e28'
        api_url = f'https://api.themoviedb.org/3/movie/{random_movie.id}/recommendations?api_key={api_key}&language=en-US&page=1'
        response = requests.get(api_url)
        recommended_movies = response.json()
        
        # 추천 영화가 있을 때
        if 'results' in recommended_movies.keys():
            recommended_movies = recommended_movies['results']

            paginator = Paginator(recommended_movies, 3)
            page = request.GET.get('page')
            posts = paginator.get_page(page)

            context = {
                'posts': posts,
                'like_movie': random_movie,
            }
            return render(request, 'accounts/recommended.html', context)
        # 추천 영화가 없을 때
        else:
            return render(request, 'accounts/no_recommendations.html')
    
    # 좋아요한 영화가 없을 때
    else:
        return render(request, 'accounts/recommended.html')