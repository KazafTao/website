from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    """User表额外信息"""
    # 使用一对一链接来扩展User模型
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 引用昵称解决User模型username不支持中文的问题
    nickname = models.CharField(verbose_name="昵称", max_length=60, blank=True, null=True)
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    gender_choice = (
        (1, '男'),
        (2, '女'),
        (3, '保密'),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choice, default=3)
    avatar = models.ImageField(verbose_name="头像路径", upload_to='avatar', default='avatar/avatar_default.png')
    background = models.ImageField(verbose_name="背景路径", upload_to='background', default='background/bg_default.png')

    def __str__(self):
        return f"{self.nickname if self.nickname else self.user.username}"


# 当User创建的实例的时候，profile自动创建实例,但是不会填充数据
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# 当User保存的时候，profile自动保存
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
