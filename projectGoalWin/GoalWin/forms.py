from django.forms import ModelForm
from django import forms

class GroupForm(forms.Form):
    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': "Group Name"}))
    desc = forms.CharField(label="Description", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': "Description"}))

    
class GoalForm(forms.Form):
    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': "Goal Name"}))
    desc = forms.CharField(label="Description", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': "Description"}))
    stake = forms.FloatField(label="Stake", widget=forms.NumberInput(attrs={'class': 'form-control','placeholder': '$ 0.00'}), min_value = 0.00)