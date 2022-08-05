from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.http import Http404
from captcha.fields import CaptchaField

from main.forms.common import BootstrapModelForm, BootstrapForm
from main.models import Profile


class RegisterForm(BootstrapModelForm):
    """注册表单"""

    class Meta:
        # 继承django自带的user模型
        model = Profile
        # 只显示username,password两个字段
        # fields = ['username', 'password', 'confirm_password', 'vcode', 'mobile']
        fields = ['username', 'password', 'confirm_password', 'mobile', 'gender']

    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=True), max_length=64)
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(render_value=True), max_length=64)

    def clean_username(self):
        """校验用户名是否已存在"""
        try:
            get_object_or_404(User, username=self.cleaned_data['username'])
            # 已存在，则校验失败
            raise ValidationError("用户名已存在")
        except Http404:
            # 不存在，则返回输入的用户名
            return self.cleaned_data['username']


def clean_confirm_password(self):
    """确保两次密码一致"""
    if self.cleaned_data["password"] == self.cleaned_data["confirm_password"]:
        return self.cleaned_data["confirm_password"]
    else:
        raise ValidationError("两次密码不一致")


class LoginForm(BootstrapForm):
    """注册表单"""
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码', widget=forms.PasswordInput, max_length=64)


class UserInfoForm(BootstrapModelForm):
    """用户信息表单"""

    class Meta:
        model = Profile
        fields = ['mobile', 'gender', 'avatar']
