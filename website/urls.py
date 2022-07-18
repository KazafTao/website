from django.contrib import admin
from django.urls import path, include


from main.views import user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user.index),
    path('login/', user.user_login),
    path('register/', user.register),
    path('logout/', user.user_logout),
    # 图片验证码
    path('captcha/', include('captcha.urls'))
]
