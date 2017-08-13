from django import forms
from allauth.account.forms import LoginForm


class MazeLoginForm(LoginForm):
    """
    Login form View
    """
    def __init__(self, *args, **kwargs):
        super(MazeLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(widget=forms.EmailInput(attrs={'id': 'email', 'required': 'required', 'class': 'form-control', 'placeholder': 'Email'}))
        self.fields['password'] = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password', 'required': 'required', 'class': 'form-control', 'placeholder': 'Password'}))
