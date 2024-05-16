from functools import wraps
from django.http import JsonResponse


def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not authenticated'}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role != 'admin':
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role != 'user':
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
# Define more custom decorators here if needed
