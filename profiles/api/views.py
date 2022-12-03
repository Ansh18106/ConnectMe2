from hashlib import new
from logging import raiseExceptions
import re
from typing import NewType
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
import random
from tweetme2.settings import ALLOWED_HOSTS


from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.utils.http import is_safe_url
from ..models import Profile
from ..serializers import PublicProfileSerializer

User = get_user_model()
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

@api_view(['GET','POST'])
def profile_detial_api_view(request, username, *args, **kwargs):
    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        return Response({'detail':"User not found"}, status=404)
    profile_obj = qs.first()
    data = request.data or {}
    if request.method == "POST":
        me = request.user
        action = data.get("action")
        if profile_obj != me:
            if action == "follow":
                profile_obj.followers.add(me)
            elif action == "unfollow":
                profile_obj.followers.remove(me)
            else:
                pass
    serailizer = PublicProfileSerializer(instance=profile_obj, context={"request": request})
    return Response(serailizer.data, status=200)


# @api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
# def user_follow_view(request,username, *args, **kwargs):
#     me = request.user
#     other_user_qs = User.objects.filter(username=username)
#     if me.username == username:
#         my_followers = profile.followers.all()
#         return Response({"count": my_followers.count()}, status=200)
#     if not other_user_qs.exists():
#         return Response({}, status=404)
#     other = other_user_qs.first()
#     profile = other.profile
#     data = request.data or {}
#     action = data.get("action")
#     if action == "follow":
#         profile.followers.add(me)
#     elif action == "unfollow":
#         profile.followers.remove(me)
#     else:
#         pass
#     # current_followers_qs = profile.followers.all()
#     data = PublicProfileSerializer(instance=profile, context={"request": request})
#     return Response(data.data, status=200)

