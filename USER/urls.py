from django.urls import path, re_path

from . import views

app_name = "USER"
urlpatterns = [
    path('register/', views.RegisterV, name='register'),
    re_path(r'^active/(?P<token>.*)/$', views.ActiveV, name='active'),
    path('active_resend/', views.Active_resendV, name='active_resend'),
    path('UserInfo/', views.UserInfoV, name='UserInfo')
]
