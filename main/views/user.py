import os

from django.shortcuts import redirect, render, resolve_url, HttpResponse, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from main.forms.user import RegisterForm, LoginForm, UserInfoForm


def register(request):
    """用户注册"""
    if request.method == "GET":
        form = RegisterForm()
        context = {
            'form': form,
        }
        return render(request, 'user/register.html', context)
    form = RegisterForm(data=request.POST)
    if form.is_valid():
        # 需要用django自带的create_user来创建用户，不能直接用form.save()，否则密码为明文
        user = User.objects.create_user(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
        # 添加用户手机
        user.profile.mobile = form.cleaned_data["mobile"]
        user.profile.gender = form.cleaned_data["gender"]
        user.save()
        messages.success(request, "注册成功")
        return redirect(resolve_url(user_login))
    # 校验不通过的重新渲染注册页面，包含将之前输入的表单数据
    return render(request, 'user/register.html', {'form': form})


def user_login(request):
    """用户登录"""
    if request.method == "GET":
        return render(request, 'user/login.html', {'form': LoginForm()})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = authenticate(**form.cleaned_data)
        if user:
            login(request, user)
            return redirect(resolve_url(index))
        else:
            messages.error(request, '用户名或密码错误')
            return render(request, 'user/login.html', {'form': form})
    return render(request, 'user/login.html', {'form': form})


def user_logout(request):
    """用户注销"""
    logout(request)
    return redirect(resolve_url(index))


@login_required()
def user_info(request):
    """用户主页"""
    profile = request.user.profile
    if request.method == "GET":
        context = {
            'form': UserInfoForm(instance=profile)
        }
        return render(request, 'user/info.html', context)
    form = UserInfoForm(data=request.POST, instance=profile)
    if form.is_valid():
        profile.mobile = form.data["mobile"]
        profile.gender = form.data["gender"]
        # 图片并不在form.data中，而是在request.FILES中
        file = request.FILES.get("avatar")
        # 将上传的文件保存到服务器上
        file_path = os.path.join(settings.MEDIA_ROOT, 'avatar/', file.name)
        with open(file_path, mode='wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        profile.avatar = file.name
        request.user.save()
        return HttpResponse("保存成功")
    else:
        print("校验失败")
        return render(request, 'user/info.html', {'form': form})


def reset_user_password(request):
    """重置密码"""
    pass


def index(request):
    """网站主页"""
    return redirect(reverse('question:index'))
