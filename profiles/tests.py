from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
# Create your tests here.
from .models import Profile

User = get_user_model()

class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Shashank', password='justAnything')
        self.user_b = User.objects.create_user(username='Shashank_', password='somethingElse')

    def test_profile_created(self):
        qs = Profile.objects.all()
        self.assertEqual(qs.count(), 2)
    
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='justAnything')
        return client

    def test_following(self):
        first = self.user
        second = self.user_b
        first.profile.followers.add(second)
        second_user_following_whom = second.following.all()
        qs = second_user_following_whom.filter(user=first) 
        first_user_following_no_one = first.following.all()
        self.assertFalse(first_user_following_no_one.exists())
        self.assertTrue(qs.exists())
    
    def test_follow_api_endpoint(self):
        client = self.get_client()
        response = client.post(
            f"/api/profiles/{self.user_b.username}/follow",
            {"action":'follow'}
        )
        r_data = response.json()
        count = r_data.get("count")
        self.assertEqual(count, 1)

    def test_unfollow_api_endpoint(self):
        first = self.user
        second = self.user_b
        first.profile.followers.add(second)
        client = self.get_client()
        response = client.post(
            f"/api/profiles/{self.user_b.username}/follow",
            {"action":'unfollow'}
        )
        r_data = response.json()
        count = r_data.get("count")
        self.assertEqual(count, 0)