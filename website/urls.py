from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from main.views import user
from website.settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    path('', user.index, name='index'),
    # 登录注册相关
    path('login/', user.user_login, name='login'),
    path('register/', user.register, name='register'),
    path('logout/', user.user_logout, name='logout'),
    # 图片验证码
    path('captcha/', include('captcha.urls')),
    path('user/info/', user.user_info, name='user_info'),
]
