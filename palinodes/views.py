from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.db import IntegrityError

from .models import User, Profile, Repository

#################__LANDING__########################

def index(request):
    return HttpResponseRedirect('dashboard')

@login_required
def dashboard(request):
     return render(request, "palinodes/dashboard.html")

def repository_view(request, repository_id):
    repository = Repository.objects.get(id=repository_id)
    return render(request, "palinodes/repository.html", {
        "repository": repository
    })

##################__APIS__##########################
#def repositories()
##################__AUTHENTICATION__################
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "palinodes/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "palinodes/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "palinodes/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Profile.objects.create(user=user)
            profile.save()
        except IntegrityError:
            return render(request, "palinodes/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "palinodes/register.html")
