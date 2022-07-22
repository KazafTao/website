from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    """User表额外信息"""
    # 使用一对一链接来扩展User模型
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(verbose_name="手机号", unique=True, max_length=11)

    def __str__(self):
        return f"手机号：{self.mobile}"


# 当User创建的实例的时候，profile自动创建实例,但是不会填充数据
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# 当User保存的时候，profile自动保存
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
