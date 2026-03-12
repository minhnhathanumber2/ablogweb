from django import forms
from django.db import models
from home.models import *

# class ParagraphForm(forms.ModelForm):
#     class Meta:
#         model = Paragraph
#         fields = ["title", "detail"]

class BlogPostForm(forms.ModelForm):
    """
    Mẫu bài viết:\n
    Tên, Ảnh (Cắt để ép ảnh 720 x 480), Danh mục, Chủ đề(Chỉ đc generate các chủ để là foreignkey của danh mục)\n
    Giới thiệu, Tiêu đề + nội dung (Là class Paragraph) \n\n

    Mỗi bài viết sẽ gồm tiêu đề, ảnh minh họa và lời giới thiệu, sẽ được hiển thị ở ngoài
    Bên trong (Tạm thời) sẽ có nhiều mục và mỗi mục có phần bổ sung, sẽ được xử lý riêng để tiếp nhận được chữ đậm, chữ nghiêng, chữ gạch chân, ...\n
    Có thể sẽ có cả ảnh\n
    """
    class Meta:
        model = BlogPost
        #fields = "__all__"
        fields = ['book_name', 'book_image', 'book_topic', 'book_description', 'book_summary']
        # #['book_name', 'book_author', 'book_image', 'book_description']
        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)

        #     self.fields["book_sub_topic"].queryset = SubTopic.objects.none()

        #     if "book_topic" in self.data:
        #         try:
        #             # category_id = int(self.data.get("category"))
        #             self.fields["book_sub_topic"].queryset = SubTopic.objects.filter(topic = int(self.data.get("book_topic")))
        #             # Product.objects.filter(
        #             #     category_id=category_id
        #             # )
        #         except (ValueError, TypeError):
        #             pass

        #     # Khi edit object
        #     elif self.instance.pk:
        #         self.fields["book_sub_topic"].queryset = SubTopic.objects.filter(topic = self.instance.book_topic)
        #         # self.fields["product"].queryset = Product.objects.filter(
        #         #     category=self.instance.category
        #         # )