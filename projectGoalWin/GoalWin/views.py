from django.shortcuts import render

# Create your views here.
def index(request):

    return render(request, "goalwin/index.html",)

# TODO
# test the following on shell:
# admins create groups, so if admin account is deleted, delete the group
# members join groups, if member account is deleted, do not delete group, just delete member
# groups can be deleted, if group is deleted, do not delete members, just delete groups and goals
# members create goals, if member is deleted, delete the goals