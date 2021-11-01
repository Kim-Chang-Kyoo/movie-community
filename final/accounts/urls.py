from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('<str:username>/recommended/', views.recommended, name='recommended'),
    path('signup/', views.signup, name='signup'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('password/', views.change_password, name='change_password'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<str:username>/', views.profile, name='profile'),
    path('follow/<int:user_pk>/', views.follow, name='follow'),
]
