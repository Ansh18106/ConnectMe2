from pydoc import cli
from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Tweet

# Create your tests here.

User = get_user_model()

class TweetTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='Shashank', password='justAnything')
        self.userb = User.objects.create_user(username='Shashank_', password='somethingElse')
        Tweet.objects.create(content='1st tweet', user=self.user)
        Tweet.objects.create(content='1st tweet', user=self.user)
        Tweet.objects.create(content='3rd tweet', user=self.userb)
        self.current_count = Tweet.objects.all().count()

    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(content='2nd tweet', user=self.user)
        self.assertEqual(tweet_obj.id, 4)
        self.assertEqual(tweet_obj.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='justAnything')
        return client

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/tweet/")
        self.assertEqual(response.status_code, 200)
        # print (response.json())
        
    def test_tweets_related_name(self):
        user = self.user
        self.assertEqual(user.tweets.count(), 2)

    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/tweet/action/", {"id":1, "action":' LIKE '})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count,1)
        user = self.user
        my_like_instances_count = user.tweetlike_set.count()
        my_related_likes = user.tweet_user.count()
        self.assertEqual(my_like_instances_count, my_related_likes)
        
    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/tweet/action/", {"id":1, "action":' LIKE '})
        self.assertEqual(response.status_code, 200)
        response = client.post("/api/tweet/action/", {"id":1, "action":'UNLIKE '})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count,0)

    def test_retweet_like(self):
        client = self.get_client()
        response = client.post("/api/tweet/action/", {"id":1, "action":' retweet '})
        self.assertEqual(response.status_code, 201)
        # response = client.post("/api/tweet/action/", {"id":1, "action":'UNLIKE '})
        # self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count,0)

        data = response.json()
        new_tweet_id = data.get("id")
        print(new_tweet_id)
        self.assertNotEqual(1, new_tweet_id)
        self.assertEqual(self.current_count+1, new_tweet_id)

    def test_tweet_create_api_view(self):
        request_data = {"content": "let's test it"}
        client = self.get_client()
        response = client.post("/api/tweet/create/", request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_tweet_id = response_data.get("id")
        self.assertEqual(self.current_count + 1, new_tweet_id)

    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/tweet/1")
        print ("456", response)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)

    def test_tweet_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/tweet/1/delete/")
        self.assertEqual(response.status_code, 200)
        client = self.get_client()
        response = client.delete("/api/tweet/1/delete/")
        self.assertEqual(response.status_code, 404)
        # response_incorrect_owner = client.delete("/api/tweet/3/delete/")
        # self.assertEqual(response_incorrect_owner.status_code, 401)