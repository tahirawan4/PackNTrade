from django import forms

class SignUpForm(forms.Form):
    name = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.Textarea)
