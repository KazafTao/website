from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from main.views import user
from website.settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user.index, name='index'),
    # 登录注册相关
    path('login/', user.user_login, name='login'),
    path('register/', user.register, name='register'),
    path('logout/', user.user_logout, name='logout'),
    path('user/info/', user.user_info, name='user_info'),
    # 问答应用
    path('question/', include('question.urls'), ),
    # 图片验证码
    path('captcha/', include('captcha.urls')),
    # 图片相关，用于直接通过浏览器url访问本地的图片
    # re_path(r'media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
]
