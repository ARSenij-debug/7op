from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class CommentForm(forms.Form):
    data = forms.CharField(max_length=1000, label="", widget=forms.Textarea, min_length=1)

    def clean_comment_data(self):
        clean_data = self.cleaned_data['data']
        if len(clean_data) == 0:
            raise ValidationError("Комментариц не должен быть пустым")
        return clean_data


class RegistrationForm(forms.Form):
    user_name = forms.CharField(max_length=100, min_length=3, label="Ваш ник")
    user_password = forms.CharField(max_length=100, min_length=8, widget=forms.PasswordInput, label="Придумайте пароль")


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, min_length=1, label="", help_text="", required=False,
                            error_messages={'required': ''})

    def clean_query(self):
        wanted_query = self.cleaned_data['query']
        if len(wanted_query) < 1:
            raise ValidationError("")
        return wanted_query
