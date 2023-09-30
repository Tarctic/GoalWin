from django.forms import ModelForm
from django import forms

from .models import User, Group, Member, Goal

class GroupForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': "Title"}))