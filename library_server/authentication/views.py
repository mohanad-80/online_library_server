from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from authentication.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        try:
            user = CustomUser.objects.get(email=email)

            # Check if the password matches
            if user.check_password(password):
                # If the password is correct, return a success response
                return JsonResponse({"user_id": user.id, "role": user.role}, status=200)
            else:
                # If the password is incorrect, return an error response
                return JsonResponse({"error": "Invalid Password"}, status=400)

        except CustomUser.DoesNotExist:
            # If the user with the provided email does not exist, return an error response
            return JsonResponse({"error": "User not found"}, status=404)

    return JsonResponse({"error": "Method Not Allowed"}, status=405)


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        first_name = data.get("fName")
        last_name = data.get("lName")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already taken"}, status=400)

        user = CustomUser.objects.create_user(email=email, role=role, password=password)

        user.first_name = first_name
        user.last_name = last_name

        user.save()

        # Return the user ID in the response
        return JsonResponse({"user_id": user.id}, status=201)

    return JsonResponse({"error": "Method Not Allowed"}, status=405)


@csrf_exempt
def edit_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get("userId")
        first_name = data.get("fName")
        last_name = data.get("lName")
        email = data.get("email")
        role = data.get("role")
        current_password = data.get("currentPassword")
        new_password = data.get("newPassword")

        try:
            user = CustomUser.objects.get(id=user_id)
            if not user.check_password(current_password):
                return JsonResponse({"error": "Incorrect password"}, status=400)

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.role = role
            if new_password:
                user.password = make_password(new_password)
            user.save()
            return JsonResponse({"message": "User updated successfully"}, status=200)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

    return JsonResponse({"error": "Method Not Allowed"}, status=405)


# @login_required
@csrf_exempt
def get_user_profile(request, user_id):
    if request.method == "GET":
        try:
            user = CustomUser.objects.get(pk=user_id)
            data = {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
            }
            return JsonResponse(data)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    else:
        return JsonResponse({"error": "Method Not Allowed"}, status=405)


@csrf_exempt
def delete_account(request, user_id):
    if request.method == "GET":
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
            return JsonResponse({"message": "Account deleted successfully"}, status=200)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    else:
        return JsonResponse({"error": "Method Not Allowed"}, status=405)
