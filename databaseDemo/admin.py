from django.contrib import admin

from USER.models import UserInfo, DatabaseRecord

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(DatabaseRecord)
