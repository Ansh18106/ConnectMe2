from django.conf import settings
from dataclasses import field
from pyexpat import model
from django import forms
from .models import  Tweet

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("This tweet is too long")
        return content