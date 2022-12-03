from hashlib import new
from logging import raiseExceptions
import re
from typing import NewType
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import random
from tweetme2.settings import ALLOWED_HOSTS

# Create your views here.
def home_view (request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)

def tweets_list_view (request, *args, **kwargs):
    return render(request, "tweets/list.html")

def tweets_detail_view (request, tweet_id, *args, **kwargs):
    return render(request, "tweets/detail.html", context={"tweet_id":tweet_id})
