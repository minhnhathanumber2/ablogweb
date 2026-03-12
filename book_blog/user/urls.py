from django.urls import path
from user import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path("", views.leaderboard_view, name="leaderboard"),
    path("<str:name>", views.profile_view, name = "profile"),
    path('logout/', LogoutView.as_view(next_page="home"), name='logout'),
]