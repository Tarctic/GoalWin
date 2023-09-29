from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Group(models.Model):
    name = models.CharField(max_length=80)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_admin")

    def __str__(self):
        return f"Group Name: {self.name}, Group admin: {self.admin}"

class Member(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_name")
    group = models.ForeignKey(Group, related_name="member_group")

    def __str__(self):
        return f"Username: {self.username}, Group: {self.group}"

class Goal(models.Model):
    setter = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="goal_setter")
    #group = models.ForeignKey(Group, related_name="goal_group")  Use if multiple groups per User
    stake = models.FloatField
    creation = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Goal setter name: {self.setter}, Stake: {self.stake}"