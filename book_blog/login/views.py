from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.contrib import messages
# from user.models import Profile
# Create your models here.
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username.replace(" ", "")) < 3:
            raise ValidationError("Tên đăng nhập cần có tối thiểu 3 kí tự và không chứa dấu cách.")
        elif len(username) > 18:
            raise ValidationError("Tên đăng nhập chỉ được tối đa 18 kí tự và không chứa dấu cách.")
        return username

def login_view(request):
    if request.user.is_authenticated: return redirect('home')
    else:
        if request.method == "POST":
            #print(request.POST)
            username_text = request.POST.get("username")[:100]
            password_text = request.POST.get("password")[:100]
            #print("user_info", username_text, password_text)
            login_user = authenticate(request, username = username_text, password = password_text)
            if login_user is not None:
                login(request, login_user)
                request.session['username'] = username_text
                return redirect('home')
            else:
                if (username_text.replace(" ", "") == ""):
                    messages.error(request, "Bạn chưa điền tên đăng nhập!")
                elif (password_text.replace(" ", "") == ""):
                    messages.error(request, "Bạn chưa điền mật khẩu!")
                else:
                    messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng")
    return render(request, "login.html")

def register_view(request):
    if request.user.is_authenticated: return redirect('home')
    form = RegisterForm()
    if request.method == "POST":
        username_text = request.POST.get("username")[:100]
        password_text = request.POST["password1"][:100]
        confirm_password_text = request.POST["password2"][:100]
        k = username_text.replace(" ", "")

        if (k == ""):
            messages.error(request, "Bạn chưa điền tên đăng nhập!")
        elif (len(k) < len(username_text)):
            messages.error(request, "Tên đăng nhập không được chứa dấu cách.")
        elif (len(k) < 3):
            messages.error(request, "Tên đăng nhập cần có tối thiểu 3 kí tự.")
        elif(len(username_text) > 18):
            messages.error(request, "Tên đăng nhập chỉ chứa tối đa 18 kí tự.")
        elif (password_text == ""):
            messages.error(request, "Bạn chưa điền mật khẩu!")
        elif (confirm_password_text == ""):
            messages.error(request, "Bạn chưa xác nhận mật khẩu!")
        elif (confirm_password_text != password_text):
            messages.error(request, "Mật khẩu xác nhận không khớp!")
        elif (len(password_text) < 8):
            messages.error(request, f"Mật khẩu phải có 8 kí tự trở lên. Mật khẩu của bạn có {len(password_text)} kí tự.")
            
        else:
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                # Profile.objects.create(user=form)
                messages.success(request, "Đăng kí thành công!")
                return redirect("login")
            else:
                messages.error(request, "Tên đăng nhập đã đã được sử dụng. Vui lòng thử một tên khác!")
    return render(request, "register.html", {'form': form})

