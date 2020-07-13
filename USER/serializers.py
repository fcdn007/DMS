from django.conf import settings
from rest_framework import serializers

from util.serializers import DynamicFieldsModelSerializer
from .models import UserInfo, DatabaseRecord


class UserInfoSerializer(DynamicFieldsModelSerializer):
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    last_login_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = UserInfo
        fields = ("username", "nick_name", "email", "password", "memo", "id", "create_time", "last_login_time")


class DatabaseRecordSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = DatabaseRecord
        fields = ("userinfo", "model_changed", "operation", "memo", "id", "last_modify_time", "create_time")
