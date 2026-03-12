from django.urls import path
from home import views


urlpatterns = [
    path('', views.home_view, name="home"),
    path('create', views.create_view, name="create"),
    path('check', views.check_view, name="check"),
    path('topic', views.all_topics_view, name="all_topics"),
    path('topic/<str:slug>', views.topic_view, name="topic"),
    path('topic/<str:slug>/<str:sub_slug>', views.sub_topic_view, name="sub_topic"),
    path('detail/<int:pk>', views.detail_view, name="detail")
]
