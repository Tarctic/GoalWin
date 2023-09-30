from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

    def __str__(self):
        return f"Group Name: {self.id}"

class Group(models.Model):
    name = models.CharField(max_length=80)
    desc = models.CharField(max_length=1000, null=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_admin")

    def __str__(self):
        return f"Group Name: {self.name}, Group admin: {self.admin}"

class Member(models.Model):
    # a profile for each user
    username = models.CharField(max_length=80)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="member_user")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name="member_group")

    def __str__(self):
        return f"Username: ({self.username}), Group: ({self.group})"

class Goal(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="goal_group")
    setter = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="goal_setter")
    #group = models.ForeignKey(Group, related_name="goal_group")  Use if multiple groups per User
    stake = models.FloatField(default=0)
    creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Goal setter name: {self.setter}, Stake: {self.stake}"