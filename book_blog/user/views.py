from django.shortcuts import render, redirect
from user.models import Profile
from django.http import Http404
from django.contrib import messages
from home.models import *
# Create your views here.
def leaderboard_view(request):
    profiles = Profile.objects.all()
    rates = []
    for profile in profiles:
        if profile.rate_changed:
            blogs = BlogPost.objects.filter(author = profile.user, state=True)
            medium_rate = 0.0
            rated_blogs = 0
            for blog in blogs:
                if blog.book_rate_times != 0:
                    rated_blogs += 1
                    medium_rate += blog.book_rate / blog.book_rate_times
            medium_rate /= rated_blogs
            rates.append(f"{medium_rate:.1f}")
            profile.rate_number = medium_rate
            profile.rate_changed = False
            profile.save()
        else:
            rates.append(f"{profile.rate_number:.1f}")
    if request.user.is_authenticated:
        return render(request, "leaderboard.html", {
            'is_user': 1,
            'user_name': request.user,
            'topics': Topic.objects.all(),
            'profiles': zip(profiles, rates),
        })
    return render(request, "leaderboard.html", {
        'is_user': 0,
        'topics': Topic.objects.all(),
        'profiles': zip(profiles, rates),
    })

def profile_view(request, name):
    profile = 0
    medium_rate_string = ""
    try:
        profile = Profile.objects.get(user__username = name)
        if profile.rate_changed:
            blogs = BlogPost.objects.filter(author = profile.user, state = True)
            medium_rate = 0.0
            rated_blogs = 0
            for blog in blogs:
                if blog.book_rate_times != 0:
                    rated_blogs += 1
                    medium_rate += blog.book_rate / blog.book_rate_times
            medium_rate /= rated_blogs
            medium_rate_string = f"{medium_rate:.1f}"
            profile.rate_number = medium_rate
            profile.rate_changed = False
            profile.save()
        else:
            medium_rate_string = f"{profile.rate_number:.1f}"
    except Profile.DoesNotExist:
        raise Http404("Vô danh ý")
    #print(profile)
    if request.user.is_authenticated:
        # print(request.user.username)
        # print(profile.user.username)
        return render(request, "profile.html", {
            'is_user': 1,
            'user_name': request.user,
            'profile': profile,
            'medium_rate_string': medium_rate_string,
            'blogs': BlogPost.objects.filter(author = profile.user, state=True).order_by("-book_rate")[:3],
        })
    return render(request, "profile.html", {
        'is_user': 0,
        'profile': profile,
        'medium_rate_string': medium_rate_string,
        'blogs': BlogPost.objects.filter(author = profile.user, state=True).order_by("-book_rate")[:3],
    })