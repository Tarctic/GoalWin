from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone

from .models import User, Member, Group, Goal
from .forms import GroupForm, GoalForm

# Create your views here.
def index(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:

        user = request.user        
        group = Member.objects.get(user=user).group

        goal = Goal.objects.get(setter=user)
        time_left = None
        if goal:
            created_month = goal.creation.month
            now = datetime.now(timezone.utc)
            if now.month==created_month:
                next_month = datetime(now.year,now.month+1,1,tzinfo=timezone.utc)
                time_left = next_month-now
            else:
                time_left = datetime(0)

        return render(request, "goalwin/index.html", {
            group: group,
            goal: goal,
            time_left: time_left
        })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


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
            return render(request, "goalwin/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "goalwin/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "goalwin/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

        except IntegrityError:
            return render(request, "goalwin/register.html", {
                "message": "Username already taken."
            })
        
        person = Member(username=username, user=user)
        person.save()

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "goalwin/register.html")
    

@login_required
def create_group(request):
    
    if request.method=="GET":
        return render(request, "GoalWin/newgroup.html", {
            "groupform" : GroupForm()
        })

    if request.method=="POST":
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        admin = request.user

        group = Group(name=name, desc=desc, admin=admin)
        group.save()

        member = Member.objects.get(user=request.user)
        member.group = group

        return HttpResponseRedirect(reverse("index"))

@login_required
def create_goal(request):

    if request.method=="GET":
        return render(request, "GoalWin/newgoal.html", {
            "goalform" : GoalForm()
        })

    if request.method=="POST":
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        stake = request.POST.get('stake')
        setter = request.user

        member = Member.objects.get(user=request.user)
        group = member.group
        
        print(member)
        print(group)

        goal = Goal(name=name, desc=desc, stake=stake, setter=setter, group=group)
        goal.save()

        return HttpResponseRedirect(reverse("index"))