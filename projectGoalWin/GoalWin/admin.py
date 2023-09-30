from django.contrib import admin

from .models import User, Group, Member, Goal
# Register your models here.

admin.site.register(User)
admin.site.register(Group)
admin.site.register(Member)
admin.site.register(Goal)