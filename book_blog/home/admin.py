from django.contrib import admin
from home.models import *
# Register your models here.
admin.site.register(Topic)
admin.site.register(SubTopic)
admin.site.register(BlogPost)
admin.site.register(Paragraph)
admin.site.register(Rate)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'author', 'like_times']
admin.site.register(Like)
