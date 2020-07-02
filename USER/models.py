import os
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("avatar", "_".join([instance.nick_name, filename]))

# Create your models here.
class UserInfo(AbstractUser):
    ROLE_CHOICES = (
        (1, '超级系统管理员'),
        (2, '项目管理员'),
        (3, '模块系统管理员'),
        (4, '普通用户'),
    )
    nick_name = models.CharField(db_column='昵称', max_length=35, blank=True, unique=True,
                                 error_messages={'nick_name_unique': "该昵称已被占用。"})
    email = models.EmailField(db_column='邮箱', unique=True, error_messages={'email_unique': "该邮箱地址已被占用。"})
    avatar = ProcessedImageField(db_column='头像', upload_to="avatar", default='avatar/default.jpg',
                                 processors=[ResizeToFill(100, 100)], format='JPEG', options={'quality': 95})
    role = models.SmallIntegerField(db_column='角色', choices=ROLE_CHOICES, default=4)
    memo = models.TextField(db_column="备注", blank=True, null=True)
    index = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(db_column='创建时间', auto_now_add=True)
    last_login_time = models.DateTimeField(db_column='最近登录时间', blank=True, null=True)

    def __str__(self):
        return self.nick_name

    class Meta(AbstractUser.Meta):
        db_table = '用户信息表'
        verbose_name = '用户'
        ordering = ["-create_time"]


# 数据库增删改记录表
class DatabaseRecord(models.Model):
    nick_name = models.ForeignKey(
        "UserInfo",
        on_delete=models.CASCADE,
        related_name='DatabaseRecord_UserInfo',
        to_field="nick_name",
        db_column='用户昵称',
        blank=True,
        null=True)
    model_changed = models.CharField(
        db_column='被变更的模型', max_length=35, blank=True, null=True)
    operation = models.CharField(
        db_column='操作', max_length=25, blank=True, null=True)
    memo = models.TextField(
        db_column='备注', blank=True, null=True)
    index = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(db_column='创建时间', auto_now_add=True)
    last_modify_time = models.DateTimeField(db_column='最近修改时间', auto_now=True)

    def __str__(self):
        return "{}对{}进行{}操作(时间为{})".format(self.nick_name, self.model_changed, self.operation, self.created)

    class Meta:
        db_table = '数据库增删改记录表'
        verbose_name = '数据库增删改记录表'
        ordering = ['-last_modify_time']

