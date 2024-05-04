from django.urls import path
# from .views import login_user, register_user, edit_user, logout_user
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('edit/', views.edit_user, name='edit'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.get_user_profile, name='profile'),
]