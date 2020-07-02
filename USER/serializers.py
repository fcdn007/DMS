from django.conf import settings
from rest_framework import serializers

from .models import UserInfo, DatabaseRecord
from util.serializers import DynamicFieldsModelSerializer


class UserInfoSerializer(DynamicFieldsModelSerializer):
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    last_login_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = UserInfo
        fields = ("username", "nick_name", "email", "password", "memo", "create_time", "last_login_time")


class DatabaseRecordSerializer(DynamicFieldsModelSerializer):
    last_modify_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)
    create_time = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required=False)

    class Meta:
        model = DatabaseRecord
        fields = ("nick_name", "model_changed", "operation", "memo", "index", "last_modify_time", "create_time")
