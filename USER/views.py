from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import Group
from itsdangerous import SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer_its
from rest_framework import viewsets

from .models import UserInfo, DatabaseRecord
from .forms import RegisterForm, UpdateForm
from .serializers import UserInfoSerializer, DatabaseRecordSerializer
from databaseDemo.tasks import send_register_active_email
from util.utils import get_queryset_base

# Create your views here.
class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    def get_queryset(self):
        return get_queryset_base(UserInfo, self.request.query_params)


class DatabaseRecordViewSet(viewsets.ModelViewSet):
    queryset = DatabaseRecord.objects.all()
    serializer_class = DatabaseRecordSerializer

    def get_queryset(self):
        return get_queryset_base(DatabaseRecord, self.request.query_params)


@never_cache
@login_required
def UserInfoV(request):
    user_old = request.user
    if request.method == 'POST':
        # user_old = None
        # if request.user.is_authenticated:
        #     user_old = request.user
        username = request.POST.get('username')
        nick_name = request.POST.get('nick_name')
        email = request.POST.get('email')
        if username == '':
            return render(request, 'USER/UserInfo.html', {'post_result': '用户名为空，请重新输入。'})
        elif user_old.username != username and UserInfo.objects.filter(username=username):
            return render(request, 'USER/UserInfo.html', {'post_result': '用户名已存在，请重新输入。'})
        elif user_old.nick_name != nick_name and UserInfo.objects.filter(nick_name=nick_name):
            return render(request, 'USER/UserInfo.html', {'post_result': '昵称已存在，请重新输入。'})
        elif user_old.email != email and UserInfo.objects.filter(email=email):
            return render(request, 'USER/UserInfo.html', {'post_result': '邮箱地址已存在，请重新输入。'})
        print("request.POST:{}".format(request.POST))
        print("request.FILES:{}".format(request.FILES))
        form = UpdateForm(data=request.POST, files=request.FILES, instance=user_old)
        if form.is_valid():
            print("form.is_valid")
            user = form.save()
            print("form.save")
            # user = UserInfo.objects.get(username=username)
            print("user: {}".format(user))
            # user.is_active = 0
            # user.role = 4
            user.save()
            context2 = {
                'nick_name': user, 'model_changed': "UserInfo",
                'operation': "修改资料成功", 'memo': "create_time: {}; role: {}".format(
                    user.create_time, user.role)
            }
            record_obj = DatabaseRecord(**context2)
            record_obj.save()
            return render(request, 'USER/UserInfo.html', {'post_result': "修改资料成功"})
        else:
            print("form.is_invalid: {}".format(form.errors))
            return render(request, 'USER/UserInfo.html', {'post_result': "%s" % form.errors})
    else:
        return render(request, 'USER/UserInfo.html')


def RegisterV(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        username = request.POST.get('username')
        nick_name = request.POST.get('nick_name')
        email = request.POST.get('email')
        if username == '':
            return render(request, 'USER/register.html', {'post_result': '用户名为空，请重新输入。'})
        elif UserInfo.objects.filter(username=username):
            return render(request, 'USER/register.html', {'post_result': '用户名已存在，请重新输入。'})
        elif UserInfo.objects.filter(nick_name=nick_name):
            return render(request, 'USER/register.html', {'post_result': '昵称已存在，请重新输入。'})
        elif UserInfo.objects.filter(email=email):
            return render(request, 'USER/register.html', {'post_result': '邮箱地址已存在，请重新输入。'})
        form = RegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            user = UserInfo.objects.get(username=username)
            group_default = Group.objects.get(name="所有模块_一般")
            user.groups.add(group_default)
            user.is_active = 0
            user.role = 4
            user.save()
            context2 = {
                'nick_name': user, 'model_changed': "UserInfo",
                'operation': "注册", 'memo': "create_time: {}; role: {}".format(user.create_time, user.role)
            }
            record_obj = DatabaseRecord(**context2)
            record_obj.save()

            # 发送激活链接，包含激活链接：(http://%s:8000/user/active/5) % SERVER_HOST
            # 激活链接中需要包含用户的身份信息，并要把身份信息进行加密
            # 激活链接格式: /user/active/用户身份加密后的信息 /user/active/token

            # 加密用户的身份信息，生成激活token
            serializer = Serializer_its(settings.SECRET_KEY, 3600)
            info = {'confirm': user.index}
            token = serializer.dumps(info)  # bytes
            token = token.decode('utf8')  # 解码, str
            # 发送邮件 celery:异步执行任务
            # print(">>>>>>>>>>>>>> user.email: %s >>>>>>>>>>>" % user.email)
            # print(">>>>>>>>>>>>>> user.username: %s >>>>>>>>>>>" % user.username)
            # print(">>>>>>>>>>>>>> token: %s >>>>>>>>>>>" % token)
            send_register_active_email.delay(user.email, user.username, token)
            if redirect_to:
                return render(request, 'USER/register.html', {'post_result': '注册成功！请查收激活邮件，激活账号后登录。',
                                                              'next': redirect_to})
            else:
                return render(request, 'USER/register.html', {'post_result': '注册成功！请查收激活邮件，激活账号后登录。',
                                                              'next': '/'})
        else:
            # print(">>>>>>>>>>>>>>>> form.errors: %s >>>>>>>>>>>>>>>>>" % form.errors)
            # print(">>>>>>>>>>>>>>>> type(form.errors): %s >>>>>>>>>>>>>>>>>" % type(form.errors))
            return render(request, 'USER/register.html', {'post_result': "%s" % form.errors})
    else:
        return render(request, 'USER/register.html')


def ActiveV(request, token):
    # 进行用户激活
    # 进行解密，获取要激活的用户信息
    serializer = Serializer_its(settings.SECRET_KEY, 3600)
    try:
        info = serializer.loads(token)
        # 获取待激活用户的id
        user_index = info['confirm']
        # 根据id获取用户信息
        user = UserInfo.objects.get(index=user_index)
        user.is_active = 1
        user.save()
        context2 = {
            'nick_name': user, 'model_changed': "User",
            'operation': "激活成功", 'memo': "无"
        }
        record_obj = DatabaseRecord(**context2)
        record_obj.save()
        # 跳转到登录页面
        return render(request, 'USER/active.html', {'success_msg': '账号已激活'})
    except SignatureExpired:
        # 激活链接已过期
        return render(request, 'USER/active.html', {'error_msg': '激活链接已过期'})
    except:
        # 激活链接已过期
        return render(request, 'USER/active.html', {'error_msg': '激活链接无效，'})


def Active_resendV(request):
    if request.method == 'POST':
        key_ = request.POST.get('name')
        value_ = request.POST.get('value')
        try:
            user = UserInfo.objects.get(**{key_: value_})
            if user.is_active:
                return JsonResponse({'error_msg': '用户已激活，请返回登录页面进行登录。'})
            else:
                # 加密用户的身份信息，生成激活token
                serializer = Serializer_its(settings.SECRET_KEY, 3600)
                info = {'confirm': user.index}
                token = serializer.dumps(info)  # bytes
                token = token.decode('utf8')  # 解码, str
                # 找其他人帮助我们发送邮件 celery:异步执行任务
                # print(">>>>>>>>>>>>>> user.email: %s >>>>>>>>>>>" % user.email)
                # print(">>>>>>>>>>>>>> user.username: %s >>>>>>>>>>>" % user.username)
                # print(">>>>>>>>>>>>>> token: %s >>>>>>>>>>>" % token)
                send_register_active_email(user.email, user.username, token)
                return render(request, 'USER/active_resend.html',
                              {'success_msg': '激活邮件发送成功！请注意查收，激活账号后登录。'})
        except UserInfo.DoesNotExist:
            return render(request, 'USER/active_resend.html', {'error_msg': '用户不存在，请重新输入。'})
    else:
        return render(request, 'USER/active_resend.html')
