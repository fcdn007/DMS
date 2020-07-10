import os
import uuid

from django.db import models


# Create your models here.
def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return os.path.join("files", "_".join([instance.uploadOperator, instance.uploadUrl, filename]))


class UploadFile(models.Model):
    uploadFile = models.FileField(
        db_column='上传文件',
        upload_to=user_directory_path,
        null=True)
    uploadUrl = models.CharField(db_column='项目', max_length=35)
    uploadOperator = models.CharField(
        db_column='上传者',
        max_length=35,
        blank=True,
        null=True)
    uploadTime = models.DateTimeField(db_column='上传时间', auto_now=True)

    def __str__(self):
        return self.uploadFile.url

    class Meta:
        db_table = '上传文件信息表'
        verbose_name = '上传文件信息表'
        permissions = [
            ("access_Advance", "Can access 高级功能"),
        ]
