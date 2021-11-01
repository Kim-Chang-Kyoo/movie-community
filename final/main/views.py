from django.shortcuts import render
from django.views.decorators.http import require_safe

# 상위 폴더에 접근하는 방법
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from movies import models as a

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from community import models as b

@require_safe
def index(request):
    # 좋아요가 많은 상위 5개 영화만 보낼거야
    movies = a.Movie.objects.order_by('-like_users')
    only_movies = []
    for movie in movies:
        if movie not in only_movies:
            only_movies.append(movie)
            if len(only_movies) == 10:
                break
    
    # 좋아요가 많은 상위 5개 리뷰만 보낼거야
    reviews = b.Review.objects.order_by('-like_users')
    only_reviews = []
    for review in reviews:
        if review not in only_reviews:
            only_reviews.append(review)
            if len(only_reviews) == 10:
                break

    context = {
        'movies': only_movies,
        'reviews': only_reviews
    }

    return render(request, 'main/index.html', context)