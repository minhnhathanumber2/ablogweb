from django.shortcuts import render, redirect
from home.models import *
from user.models import *
from home.forms import BlogPostForm
from django.http import Http404, JsonResponse
from django.contrib import messages
from book_blog.text import return_for_hacker, get_id_number_shuffle
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
# Create your views here.
def home_view(request):
    if request.user.is_authenticated: 
        return render(request, "home.html", {
            'is_user': 1,
            'user_name': request.user,
            'recent_post':BlogPost.objects.filter(state=True).order_by("-compare_update_date")[:3],
            'topics': Topic.objects.all(),
        })
    else:
        return render(request, "home.html", {
            'is_user': 0,
            'recent_post':BlogPost.objects.filter(state=True).order_by("-compare_update_date")[:3],
            'topics': Topic.objects.all(),
        })

def create_view(request):
    if request.user.is_authenticated:
        blog_post_form = BlogPostForm(prefix = "blog_post")
        # paragraph_form = ParagraphForm(prefix = "paragraph")
        if request.method == "POST":
            blog_post_form = BlogPostForm(request.POST, request.FILES, prefix = "blog_post")
            paragraph_title_forms = request.POST.getlist("paragraph-title")
            paragraph_detail_forms = request.POST.getlist("paragraph-detail")
            #paragraph_form = ParagraphForm(request.POST, request.FILES, prefix = "paragraph") #<- Truyền request.FILES khi ko có file cx ko sao
            # print(form)
            # print(form["book_image"])
            post = blog_post_form.save(commit=False)
            post.author = request.user
            post.save()
            for i in range(len(paragraph_title_forms)):
                if paragraph_title_forms[i] and paragraph_detail_forms[i]:
                    Paragraph.objects.create(
                        index = i + 1,
                        blog = post,
                        title = paragraph_title_forms[i],
                        detail = paragraph_detail_forms[i],
                    )
            #blog_post_form.save_m2m() #Lưu Model có ManyToManyField phải có cái này, ko thì lượn
            return redirect("home")

        return render(request, "create.html", {
            'is_user': 1,
            'user_name': request.user,
            'blog_form': blog_post_form,
            #'paragraph_form': paragraph_form,
            'topics': Topic.objects.all(),
        })
    else:
        return redirect("login")

def all_topics_view(request):
    topics = Topic.objects.all()
    blogs = []
    for topic in topics:
        #topic_blog = Topic.objects.get(slug=topic.slug).blogpost_set.filter(state=True).order_by("-rate")[:6]
        topic_blog = BlogPost.objects.filter(state=True, book_topic=topic).order_by("-book_rate")[:6]
        blogs.append(topic_blog)

    if request.user.is_authenticated: 
        return render(request, "all_topics.html", {
            'is_user': 1,
            'user_name': request.user,
            'topics': topics,
            'high_rate_blogs':BlogPost.objects.filter(state=True).order_by("-book_rate")[:3],
            # 'blogs:': blogs,
            'topics_blogs_item': zip(topics, blogs),
        })
    else:
        return render(request, "all_topics.html", {
            'is_user': 0,
            'topics': topics,
            'high_rate_blogs':BlogPost.objects.filter(state=True).order_by("-book_rate")[:3],
            # 'blogs:': blogs,
            'topics_blogs_item': zip(topics, blogs),
        })
def topic_view(request, slug):
    big_topic = get_object_or_404(Topic, slug=slug)
    blogs = []
    topics = SubTopic.objects.filter(topic=big_topic)
    for topic in topics:
        topic_blog = SubTopic.objects.get(slug=topic.slug).blogpost_set.filter(state=True).order_by("-book_rate")[:4]
        #blogpost_set là related_name mặc định của Django để truy xuất ngược ra các BlogPost có chứa Topic đó
        #muốn custom thì sửa related_name ở model
        blogs.append(topic_blog)
    if request.user.is_authenticated: 
        return render(request, "topic.html", {
            'is_user': 1,
            'user_name': request.user,
            'big_topic': big_topic,
            'topics': Topic.objects.all(),
            'high_rate_blogs':BlogPost.objects.filter(book_topic=big_topic, state=True).order_by("-book_rate")[:3],
            # 'blogs:': blogs,
            'topics_blogs_item': zip(topics, blogs),
        })
    else:
        return render(request, "topic.html", {
            'is_user': 0,
            'topics': Topic.objects.all(),
            'big_topic': big_topic,
            'high_rate_blogs':BlogPost.objects.filter(book_topic=big_topic, state=True).order_by("-book_rate")[:3],
            # 'blogs:': blogs,
            'topics_blogs_item': zip(topics, blogs),
        })
def sub_topic_view(request, slug, sub_slug):
    topic = SubTopic.objects.get(slug=sub_slug)
    blogs = topic.blogpost_set.filter(state=True).order_by("-book_rate")
    if request.user.is_authenticated: 
        return render(request, "sub_topic.html", {
            'is_user': 1,
            'user_name': request.user,
            'topics': Topic.objects.all(),
            'high_rate_blogs':blogs[:3],
            'topic': topic,
            'blogs': blogs,
        })
    else:
        return render(request, "sub_topic.html", {
            'is_user': 0,
            'topics': Topic.objects.all(),
            'high_rate_blogs':blogs[:3],
            'topic': topic,
            'blogs': blogs,
        })

def detail_view(request, pk):
    requested_id = get_id_number_shuffle(pk)
    blog = 0
    try:
        blog = BlogPost.objects.get(id = requested_id)
    except BlogPost.DoesNotExist:
        raise Http404("Blog ko có, đừng vào!")
    if not blog.state and (not request.user.is_staff and blog.author != request.user):
        raise Http404("Ko phải staff hay tác giả thì đừng vào!")
    if request.user.is_staff:
        if request.method == "POST":
            if not blog.state:
                option = request.POST.get("state_select")
                if (option == "keep"):
                    blog.state = True
                    blog.save()
                    blog_author = Profile.objects.get(user = blog.author)
                    blog_author.post_number += 1
                    blog_author.save()
                    messages.success(request, "Đã chấp nhận blog!")
                elif (option == "remove"):
                    blog.delete()
                    messages.success(request, "Đã từ chối blog!")
                return redirect("check")
            else:
                comment_option = request.POST.get("comment_submit")
                rate_option = request.POST.get("rate_submit")
                like_option = request.POST.get("like_submit")
                if rate_option:
                    if not rate_option.isdigit():
                        return JsonResponse({"success": False, "message": f"{return_for_hacker()}"})
                    rate_number = int(rate_option)
                    if not rate_number in [1, 2, 3, 4, 5]:
                        return JsonResponse({"success": False, "message": f"{return_for_hacker()}"})
                    try:
                        rate = Rate.objects.get(user=request.user, blog=blog)
                        
                        blog.book_rate_times -= 1
                        blog.book_rate -= rate.rate
                        rate.delete()
                        blog.save()
                    except Rate.DoesNotExist:
                        pass
                    Rate.objects.create(user=request.user, blog=blog, rate=rate_number)
                    blog.book_rate_times += 1
                    blog.book_rate += rate_number
                    blog.save()
                    blog_author = Profile.objects.get(user = blog.author)
                    blog_author.rate_changed = True
                    blog_author.save()
                    return JsonResponse({
                        "success": True,
                        "rate":rate_number,
                        "rate_time":blog.book_rate_times,
                        "medium_rate":blog.book_medium_rate(),
                    })
                elif comment_option == "comment":
                    comment_text = request.POST.get("comment_text")
                    if not comment_text:
                        messages.error(request, "Bạn chưa viết bình luận!")
                    else:
                        Comment.objects.create(
                            blog=blog,
                            comment=comment_text,
                            author= request.user,
                        )
                        blog.book_comment_times += 1
                        blog.save()
                        return redirect("detail", pk=blog.id_number_shuffle())
                elif like_option:
                    like_comment = 0
                    if not like_option.isdigit():
                        return JsonResponse({"success": False, "message": f"{return_for_hacker()}"})
                    try:
                        like_comment = Comment.objects.get(id=like_option)
                    except Comment.DoesNotExist:
                        return JsonResponse({"success": False, "message": f"{return_for_hacker()}"})
                    try:
                        like = Like.objects.get(comment = like_comment, user = request.user)
                        like.delete()
                        like_comment.like_times -= 1
                        like_comment.save()
                        return JsonResponse({
                            "success": True,
                            "is_liked": False,
                            "new_like_count": like_comment.like_times,
                            "comment_id": like_comment.id
                        })
                    except Like.DoesNotExist:
                        like = Like.objects.create(
                            comment = like_comment,
                            user = request.user
                        )
                        like_comment.like_times += 1
                        like_comment.save()
                        return JsonResponse({
                            "success": True,
                            "is_liked": True,
                            "new_like_count": like_comment.like_times,
                            "comment_id": like_comment.id
                        })
        comments = Comment.objects.filter(blog=blog)[:5]
        user_state = []
        for comment in comments:
            try:
                Like.objects.get(comment = comment, user = request.user)
                user_state.append(True)
            except Like.DoesNotExist:
                user_state.append(False)
        rate = 0
        try:
            rate = Rate.objects.get(blog=blog, user=request.user).rate
        except Rate.DoesNotExist:
            pass
        return render(request, "detail.html",{
            'is_user': 1,
            'user_name': request.user,
            'topics': Topic.objects.all(),
            'comments': zip(user_state, comments),
            'rate': rate,
            'high_rate_blogs': BlogPost.objects.filter(author=blog.author, state=True).exclude(id=requested_id).order_by("-compare_update_date")[:3],
            'blog': blog,
            'paragraphs': Paragraph.objects.filter(blog=blog).order_by("index"),
            'sub_topics': blog.book_sub_topic.all(),
        })
    elif request.user.is_authenticated:
        if request.method=="POST":
            comment_option = request.POST.get("comment_submit")
            rate_option = request.POST.get("rate_submit")
            like_option = request.POST.get("like_submit")
            if rate_option:
                if not rate_option.isdigit():
                    return JsonResponse({"success": False, "message": f"{return_for_hacker()}"})
                rate_number = int(rate_option)
                if not rate_number in [1, 2, 3, 4, 5]:
                    return JsonResponse({"success": False, "message": f"{return_for_hacker()}"})
                try:
                    rate = Rate.objects.get(user=request.user, blog=blog)
                    blog.book_rate_times -= 1
                    blog.book_rate -= rate.rate
                    rate.delete()
                    blog.save()
                except Rate.DoesNotExist:
                    pass
                Rate.objects.create(user=request.user, blog=blog, rate=rate_number)
                blog.book_rate_times += 1
                blog.book_rate += rate_number
                blog.save()
                blog_author = Profile.objects.get(user = blog.author)
                blog_author.rate_changed = True
                blog_author.save()
                return JsonResponse({
                    "success": True,
                    "rate":rate_number,
                    "rate_time":blog.book_rate_times,
                    "medium_rate":blog.book_medium_rate(),
                })
            if comment_option == "comment":
                comment_text = request.POST.get("comment_text")[:500]
                if not comment_text:
                    messages.error(request, "Bạn chưa viết bình luận!")
                else:
                    Comment.objects.create(
                        blog=blog,
                        comment=comment_text,
                        author= request.user,
                    )
                    blog.book_comment_times += 1
                    blog.save()
                    return redirect("detail", pk=blog.id_number_shuffle())
            elif like_option:
                like_comment = 0
                if not like_option.isdigit():
                    return JsonResponse({"success": False, "message": f"{return_for_hacker()}"})
                try:
                    like_comment = Comment.objects.get(id=like_option)
                except Comment.DoesNotExist:
                    return JsonResponse({"success": False, "message": f"{return_for_hacker()}"})
                try:
                    like = Like.objects.get(comment = like_comment, user = request.user)
                    like.delete()
                    like_comment.like_times -= 1
                    like_comment.save()
                    return JsonResponse({
                        "success": True,
                        "is_liked": False,
                        "new_like_count": like_comment.like_times,
                        "comment_id": like_comment.id
                    })
                except Like.DoesNotExist:
                    like = Like.objects.create(
                        comment = like_comment,
                        user = request.user
                    )
                    like_comment.like_times += 1
                    like_comment.save()
                    return JsonResponse({
                        "success": True,
                        "is_liked": True,
                        "new_like_count": like_comment.like_times,
                        "comment_id": like_comment.id
                    })
        comments = Comment.objects.filter(blog=blog)[:5]
        user_state = []
        for comment in comments:
            try:
                Like.objects.get(comment = comment, user = request.user)
                user_state.append(True)
            except Like.DoesNotExist:
                user_state.append(False)
        rate = 0
        try:
            rate = Rate.objects.get(blog=blog, user=request.user).rate
        except Rate.DoesNotExist:
            pass
        return render(request, "detail.html",{
            'is_user': 1,
            'user_name': request.user,
            'topics': Topic.objects.all(),
            'comments': zip(user_state, comments),
            'rate': rate,
            'high_rate_blogs': BlogPost.objects.filter(author=blog.author, state=True).exclude(id=requested_id).order_by("-compare_update_date")[:3],
            'blog': blog,
            'paragraphs': Paragraph.objects.filter(blog=blog).order_by("index"),
            'sub_topics': blog.book_sub_topic.all(),
        })
    else:
        comments = Comment.objects.filter(blog=blog)[:5]
        user_state = []
        for i in range(len(comments)): user_state.append(False)

        return render(request, "detail.html", {
            'is_user': 0,
            'topics': Topic.objects.all(),
            'comments': zip(user_state, comments), # Model đã order theo compare date
            'high_rate_blogs': BlogPost.objects.filter(author=blog.author, state=True).exclude(id=requested_id).order_by("-compare_update_date")[:3],
            'blog': blog,
            'paragraphs': Paragraph.objects.filter(blog=blog).order_by("index"),
            'sub_topics': blog.book_sub_topic.all(),
        })

def check_view(request):

    if request.user.is_authenticated:
        if request.user.is_staff:
            post_list = BlogPost.objects.filter(state=False)
             
            if request.method == "POST":
                option = request.POST.get("state_select")
                #post_id = 
                post_id = request.POST.get("post_id")
                if not post_id.isdigit():
                    messages.error(request, return_for_hacker())
                try:
                    cur_post = BlogPost.objects.get(id=post_id)
                    if (option == "keep"):
                        cur_post.state = True
                        cur_post.save()
                        blog_author = Profile.objects.get(user = cur_post.author)
                        blog_author.post_number += 1
                        blog_author.save()
                    else:
                        cur_post.delete()
                except BlogPost.DoesNotExist:
                    messages.error(request, return_for_hacker())
                    # if (option == "keep"):
                    #     cur_post = BlogPost.objects.get("")

            return render(request, "check.html", {
                'is_user': 1,
                'user_name': request.user,
                "post_list": post_list,
                'topics': Topic.objects.all(),
            })
        raise Http404("Người dưới 18 tuổi không được truy cập vào trang này!")
    else:
        return redirect("login")