from django.urls import path
# from .views import login_user, register_user, edit_user, logout_user
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('edit/', views.edit_user, name='edit'),
    path('profile/<int:user_id>/', views.get_user_profile, name='profile'),
    path('delete/<int:user_id>/', views.delete_account, name='deleteAccount'),
]