from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt
import os
import requests

# Create your views here.
def root(request):
    return render(request, "index.html")

def register(request):
    return render(request, "register.html")

def register_account(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == "first_name":
                messages.error(request, value, extra_tags="first_name")
            if key == "last_name":
                messages.error(request, value, extra_tags="last_name")
            if key == "reg_email":
                messages.error(request, value, extra_tags="reg_email")
            if key == "reg_password":
                messages.error(request, value, extra_tags="reg_password")
            if key == "confirm_pw":
                messages.error(request, value, extra_tags="confirm_pw")
        return redirect("/register")
    else:
        hashed_password = bcrypt.hashpw(
            request.POST["reg_password"].encode(), bcrypt.gensalt()
        ).decode()
        user = User.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["reg_email"],
            password=hashed_password,
        )
        request.session["user_id"] = user.id
        return redirect("/home")


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == "log_email":
                messages.error(request, value, extra_tags="log_email")
            if key == "log_password":
                messages.error(request, value, extra_tags="log_password")
        return redirect("/")
    else:
        user_list = User.objects.filter(email=request.POST["log_email"])
        if len(user_list) == 0:
            messages.error(request, "Email address not found.", extra_tags="log_email")
            return redirect("/")
        else:
            user = user_list[0]
            if bcrypt.checkpw(
                request.POST["log_password"].encode(), user.password.encode()
            ):
                request.session["user_id"] = user.id
                return redirect("/home")
            else:
                messages.error(
                    request, "Incorrect password.", extra_tags="log_password"
                )
                return redirect("/")


def home(request):
    if "user_id" not in request.session:
        return redirect("/")
    else:
        # base_url = 'https://api.themoviedb.org/3/movie/76341?'
        # api_key = os.environ['API_KEY']

        # r = request.GET(f'{base_url}&appid={api_key}').json()
        # print(r)
        context = {
            "user": User.objects.get(id=request.session["user_id"])
            }
    return render(request, "home.html", context)

def search(request):
    # search_title = request.POST['search']
    return redirect ('/results')

def results(request):

    return render(request, 'results.html')

def title_details(request):

    return render(request, 'title_details.html')




def logout(request):
    request.session.flush()
    return redirect("/")

