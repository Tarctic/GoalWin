from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone, timedelta

from .models import User, Member, Group, Goal
from .forms import GroupForm, GoalForm

# Create your views here.
def index(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:

        user = request.user        
        group = Member.objects.get(user=user).group
        group_name = groups = None
        if group:
            group_name = group.name
        else:
            groups = list(Group.objects.values_list('name', flat=True))

        members_count = Member.objects.filter(group=group).count()
        completed_goals_count = Goal.objects.filter(group=group, completed=True).count()

        user_winnings = 0  # this is if no group, no goal set or goal not completed, otherwise value will be modified later below
        user_completed = None

        try:
            goal = Goal.objects.get(setter=user)
        except:
            goal = goal_name = time_left = stake = None
            
        time_left = None
        if goal:
            goal_name = goal.name
            created_month = goal.creation.month
            now = datetime.now(timezone.utc)
            stake = goal.stake
            user_completed = goal.completed

            # TEST results and completion view - change minute count to whenever you will be ready to test
            # test_time = datetime(now.year,now.month,now.day,now.hour,32,tzinfo=timezone.utc)
            # print("is there time left?", now<=test_time)
            # if now<=test_time: # NOT TIME YET

            if now.month==created_month:
                next_month = datetime(now.year,now.month+1,1,tzinfo=timezone.utc)
                time_left = next_month-now
                print("Has user completed goal?", user_completed)

            else: # TIME TO SHOW
                time_left = 0
                
                if user_completed:
                    uncompleted_goals = Goal.objects.filter(group=group, completed=False)
                    uncompleted_stakes = 0
                    for goal in uncompleted_goals:
                        uncompleted_stakes += goal.stake
                    divided_winnings = uncompleted_stakes/completed_goals_count
                    user_winnings = goal.stake + divided_winnings
                

        return render(request, "goalwin/index.html", {
            "group": group_name,
            "groups": groups,
            "goal": goal_name,
            "time_left": time_left,
            "stake": stake,
            "total_members":members_count,
            "completed_members":completed_goals_count,
            "user_completed": user_completed,
            "user_winnings": user_winnings,
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
        member.save()

        return HttpResponseRedirect(reverse("index"))
    
@login_required
def join_group(request, joining_group):

    if request.method=="GET":
        member = Member.objects.get(user=request.user)
        group = Group.objects.get(name=joining_group)
        member.group = group
        member.save()

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

@login_required
def goal_completed(request):
    
    if request.method=="GET":
        goal = Goal.objects.get(setter=request.user)  # if user can join multiple groups, add group=group condition
        goal.completed = True
        goal.save()

        return HttpResponseRedirect(reverse("index"))