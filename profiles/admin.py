from django.contrib import admin

from .models import Profile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    # inlines = [TweetLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['content' ,'user__username']
    class Meta:
        model = Profile

admin.site.register(Profile, ProfileAdmin)