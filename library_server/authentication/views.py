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

        user = CustomUser.objects.filter(email=email).exists()
        if not user:
            return JsonResponse({"error": "Invalid Email"}, status=400)

        authUser = authenticate(email=email, password=password)

        request.session["role"] = user.role
        request.session["email"] = email

        if authUser is None:
            return JsonResponse({"error": "Invalid Password"}, status=400)
        else:
            login(request, user)
            return JsonResponse({"message": "Login Successful"}, status=200)

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

        # user = CustomUser.objects.create_user(
        #     first_name=first_name,
        #     last_name=last_name,
        #     email=email,
        #     username=email,  # Set email as username
        #     role=role,
        # )

        # user.set_password(password)
        # user.save()

        # Create a new CustomUser object
        user = CustomUser.objects.create_user(email=email, role=role, password=password)

        # Set additional fields
        user.first_name = first_name
        user.last_name = last_name
        user.username = email  # Set email as username

        # Save the user object
        user.save()

        # Authenticate user after registration
        authUser = authenticate(email=email, password=password)
        request.session["role"] = role
        request.session["email"] = email

        if authUser is not None:
            login(request, user)
            return JsonResponse({"message": "Account created Successfully"}, status=201)
        else:
            return JsonResponse({"error": "Authentication failed"}, status=400)

    return JsonResponse({"error": "Method Not Allowed"}, status=405)


@csrf_exempt
def edit_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # user_id = data.get("user_id")
        first_name = data.get("fName")
        last_name = data.get("lName")
        email = data.get("email")
        role = data.get("role")
        new_password = data.get("new_password")

        try:
            user = CustomUser.objects.get(email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.role = role
            if new_password:
                user.password = make_password(new_password)
            user.save()
            request.session["role"] = role
            request.session["email"] = email
            return JsonResponse({"message": "User updated successfully"}, status=200)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

    return JsonResponse({"error": "Method Not Allowed"}, status=405)


@csrf_exempt
def logout_user(request):
    if request.method == "POST":
        logout(request)
        request.session.flush()
        return JsonResponse({"message": "Logout Successful"}, status=200)

    return JsonResponse({"error": "Method Not Allowed"}, status=405)


# @login_required
@csrf_exempt
def get_user_profile(request):
    print(request.user)
    if request.session:
        email = request.session.get("email")
        print(email)
        user = CustomUser.objects.filter(email=email)
        print(user)
        data = {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "User is not authenticated"}, status=401)
