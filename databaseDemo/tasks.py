import datetime
import subprocess

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q

from USER.models import UserInfo, DatabaseRecord
from util.merge_df import make_new_merge_df_all, make_new_merge_df_partly, check_new_merge_df_all
from .celerys import app
from .settings import SERVER_HOST, BASE_DIR


@app.task
def send_register_active_email(to_email, username, token):
    """发送激活邮件"""
    # 组织邮件信息
    subject = '华大数极数据库管理系统'
    message = ''
    sender = settings.EMAIL_PROM  # 发送人
    receiver = [to_email]
    html_message = '<h1>%s, 欢迎您成为华大数极数据库管理系统注册成员</h1>请点击下面链接激活您的账户<br/>' \
                   '<a href="http://%s:8000/USER/active/%s">http://%s:8000/USER/active/%s</a>' % \
                   (username, SERVER_HOST, token, SERVER_HOST, token)

    send_mail(subject, message, sender, receiver, html_message=html_message)
    return True
    # time.sleep(5)


@app.task
def make_new_merge_df_partly_by_celery(json_files_tmp, time2, index):
    make_new_merge_df_partly(json_files_tmp, time2, index)
    return True


@shared_task
def keep_merge_df_newest_by_celery():
    flag_update_list, time2_list, json_files_list = check_new_merge_df_all()
    check_new_list = []
    for i in range(len(flag_update_list)):
        if flag_update_list[i]:
            make_new_merge_df_partly(json_files_list[i], time2_list[i], i)
            check_new_list.append(False)
        else:
            check_new_list.append(True)

    if False in check_new_list:
        make_new_merge_df_all(time2_list, json_files_list)
    return True


@shared_task
def backup_db_by_celery():
    subprocess.run(" ".join(["cd", BASE_DIR, "&&", "bash", "bkdb.sh"]), shell=True)
    return True


@shared_task
def add_modelViewRecord_by_celery(model_, username):
    user = UserInfo.objects.get(username=username)
    last_record = DatabaseRecord.objects.filter(Q(model_changed=model_) & Q(userinfo=user) & Q(operation="访问")
                                                ).order_by("-create_time")
    now = datetime.datetime.now()
    create_bool = True
    try:
        if (now - last_record[0].create_time.replace(tzinfo=None)).seconds < 60:
            create_bool = False
    except IndexError:
        pass

    if create_bool:
        new_record = {
            'userinfo': user, 'model_changed': model_,
            'operation': "访问",
            'memo': "无"
        }
        record_obj = DatabaseRecord(**new_record)
        record_obj.save()
    return True
