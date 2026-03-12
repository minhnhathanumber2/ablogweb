from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
    

class Topic(models.Model):
    """
    Cho chủ đề chính
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    def __str__(self):
        return self.name

class SubTopic(models.Model):
    """
    Cho chủ đề phụ trong mỗi loại blog
    """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    def __str__(self):
        return self.name

class BlogPost(models.Model):
    """
    大好き、だから、僕と付き合ってくれませんか。🫶🫶🫶🫶🫶
    """
    class Meta:
        ordering = ['-compare_update_date']
    book_name = models.CharField(max_length=200)
    # book_author = models.CharField(max_length=255)
    book_image = models.ImageField(upload_to='book_images/', default='default_book.png')
    book_topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    book_sub_topic = models.ManyToManyField(SubTopic, blank=True)
    book_description = models.TextField(default="")
    book_summary = models.TextField(default="")
    #below are fields which won't appear in create.html
    book_rate = models.IntegerField(default=0)
    book_rate_times = models.IntegerField(default=0)
    book_comment_times = models.IntegerField(default=0)
    update_date = models.DateField(default=now)
    compare_update_date = models.DateTimeField(default=now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.BooleanField(default=False)
    def __str__(self):
        return self.book_name
    
    def id_number_shuffle(self):
        """
        Xáo ID
        """
        num = (138432 - self.id) * 5 + 853647
        return num
    def book_medium_rate(self):
        """
        Hiện rate
        """
        if self.book_rate_times > 0:
            num = self.book_rate / self.book_rate_times
            return f"{num:.1f}"
        return f"0.0"
    # def get_absolute_url(self):
    #     return reverse("detail", args=[str(self.id)])
class Paragraph(models.Model):
    """
    Đoạn văn
    """
    class Meta:
        ordering = ['index']
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    index = models.IntegerField(default=0)
    title = models.CharField(max_length=100, default="")
    detail = models.TextField(default="")

class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)
    date = models.DateField(default=now)
    compare_date = models.DateTimeField(default=now)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'blog'],
                name='unique_user_blog'
            )
        ] #Đống này thay cho cái: unique_together = ('user', 'blog')
    

class Comment(models.Model):
    """
    本当に、ノーコメント
    """
    class Meta:
        ordering = ['-compare_date']
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(default="")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=now)
    compare_date = models.DateTimeField(default=now)
    like_times = models.IntegerField(default=0)
    def __str__(self):
        return self.comment
   
    def get_absolute_url(self):
        return reverse("detail",args=[str(self.blog.id)])

class Like(models.Model):
    """
    Like and Subscribe!!!!
    """
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'comment'],
                name='unique_user_comment'
            )
        ]
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
