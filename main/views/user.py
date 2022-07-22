from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from main.forms.user import RegisterForm, LoginForm, ProfileForm


def register(request):
    """用户注册"""
    if request.method == "GET":
        form = RegisterForm()
        # 取消验证码
        # form.fields.pop('vcode')
        context = {
            'form': form,
        }
        return render(request, 'user/register.html', context)
    form = RegisterForm(data=request.POST)
    if form.is_valid():
        # create_user函数没有confirm_password和vcode参数
        form.cleaned_data.pop('confirm_password')
        mobile = form.cleaned_data.pop('mobile')
        # form.cleaned_data.pop('vcode')
        # 需要用django自带的create_user来创建用户，不能直接用form.save()，否则密码为明文
        user = User.objects.create_user(**form.cleaned_data)
        # 添加用户手机
        user.profile.mobile = mobile
        user.save()
        return redirect('/login/')
    # 校验不通过的重新渲染注册页面，包含将之前输入的表单数据
    # 取消验证码
    print(form.errors)
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
            return redirect('/')
        else:
            messages.error(request, '用户名或密码错误')
            return render(request, 'user/login.html', {'form': form})
    return render(request, 'user/login.html', {'form': form})


def user_logout(request):
    """用户注销"""
    logout(request)
    return redirect('/')


# @login_required()
def index(request):
    # return render(request, 'layout.html')
    return render(request, 'user/test.html')
