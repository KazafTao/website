from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from main.forms.common import BootstrapModelForm, BootstrapForm


class RegisterForm(BootstrapModelForm):
    """注册表单"""

    class Meta:
        # 继承django自带的user模型
        model = User
        # 只显示username,password两个字段
        fields = ['username', 'password', 'confirm_password', 'vcode']

    password = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=True), max_length=64)
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput(render_value=True), max_length=64)
    vcode = CaptchaField(label='验证码')

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