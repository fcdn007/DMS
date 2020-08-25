import base64
import hashlib
import json
import os
import re

import pandas as pd
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

from ADVANCE.models import UploadFile
from USER.models import UserInfo, DatabaseRecord
from databaseDemo.settings import WOPI_FILE_DIR, SERVER_HOST
from util.merge_df import save_records


@csrf_exempt
def file_iterator(filename, chunk_size=512):
    # read file
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def getFilePath(fileid, user_id, cp_bool=False):
    file_path_raw = os.path.join(WOPI_FILE_DIR)
    file_path = "{}.userid{}{}".format(os.path.splitext(file_path_raw)[0], user_id,
                                       os.path.splitext(file_path_raw)[1])
    # print(">>>file_path_raw: {};file_path: {}".format(file_path_raw, file_path))
    if fileid.startswith("queryset"):
        file_path_raw = os.path.join(file_path_raw, "user", fileid)
        file_path = file_path_raw
    else:
        file_path_raw = os.path.join(file_path_raw, "mysql", fileid)
        file_path = "{}.userid{}{}".format(os.path.splitext(file_path_raw)[0], user_id,
                                           os.path.splitext(file_path_raw)[1])
        file_path = re.sub(r'mysql', "user", file_path)
        if cp_bool:
            os.system('cp {} {}'.format(file_path_raw, file_path))

    return [file_path_raw, file_path]

@csrf_exempt
def wopiGetFileInfo(request, fileid='test.txt'):
    # Get file info. Implements the CheckFileInfo WOPI call
    # print('Get file info. Implements the CheckFileInfo WOPI call')
    user_id = int(request.GET.get('access_token').split('_')[0])
    file_path_raw, file_path = getFilePath(fileid, user_id, cp_bool=True)
    # print(">>>file_path_raw: {};file_path: {}".format(file_path_raw, file_path))
    rf = open(file_path, 'rb')
    f = rf.read()
    # user = UserInfo.objects.get(id=user_id)
    json_data = {'BaseFileName': fileid, 'OwnerId': user_id, 'Size': len(f)}
    dig = hashlib.sha256(f).digest()
    json_data['SHA256'] = base64.b64encode(dig).decode()
    json_data['Version'] = '1'
    json_data['SupportsUpdate'] = True
    json_data['UserCanWrite'] = True if request.GET.get('access_token').split('_')[1] else False
    json_data['SupportsLocks'] = True
    # print(">>>json_data: {}".format(json_data))
    return HttpResponse(json.dumps(json_data, ensure_ascii=False), content_type='application/json; charset=utf-8')


@csrf_exempt
def wopiFileContents(request, fileid='test.txt'):
    # Request to file contents, Implements the GetFile WOPI call
    # print('Request to file contents, Implements the GetFile WOPI call')
    user_id = int(request.GET.get('access_token').split('_')[0])
    file_path_raw, file_path = getFilePath(fileid, user_id)
    # print(">>>file_path_raw: {};file_path: {}".format(file_path_raw, file_path))
    if request.method == 'GET':
        print('get file contents')
        response = StreamingHttpResponse(file_iterator(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(fileid)
        # print(">>>file_path_raw: {};file_path: {}".format(file_path_raw, file_path))
        return response
    elif request.method == 'POST':
        # print('Update file with new contents. Implements the PutFile WOPI call')
        with open(file_path, 'wb+') as f:
            f.write(request.body)
            f.close()
        # compare file_path with file_path_raw, generate file_path_diff_upload
        df_raw = pd.read_excel(file_path_raw, header=0, encoding='utf-8')
        df_new = pd.read_excel(file_path, header=0, encoding='utf-8')
        df_diff = pd.concat([df_raw, df_new]).drop_duplicates(keep=False)
        df_diff = pd.concat([df_raw, df_diff]).drop_duplicates(keep=False)
        if df_diff.shape[0] > 0:
            diff_file_path = re.sub(r'/user/', '/upload/', file_path)
            df_diff.to_excel(diff_file_path, index=False)
            upload_file = UploadFile(
                uploadFile=diff_file_path,
                uploadUrl=os.path.split(diff_file_path)[-1].split(".")[0],
                uploadOperator=request.user.username
            )
            upload_file.save()
            user = UserInfo.objects.get(id=user_id)
            total, valid, add, warning, error_msg, fatal_error = save_records(upload_file)
            if fatal_error:
                context2 = {
                    'userinfo': user, 'model_changed': upload_file.uploadUrl,
                    'operation': "批量上传失败",
                    'memo': "file_path: {};fatal_error: {}".format(upload_file.uploadFile.path, fatal_error)
                }
            else:
                context2 = {
                    'userinfo': user, 'model_changed': upload_file.uploadUrl,
                    'operation': "批量上传成功",
                    'memo': "file_path: {};all_records: {};valid_records: {};error_msg_tolerant: {}".format(
                        upload_file.uploadFile.path, total, valid, error_msg)
                }
            record_obj = DatabaseRecord(**context2)
            record_obj.save()
            os.system('rm {}'.format(diff_file_path))
        os.system('rm {}'.format(file_path))
        # print(">>>file_path_raw: {};file_path: {};diff_file_path: {}".format(file_path_raw, file_path,
        # diff_file_path))
        return HttpResponse('')


@csrf_exempt
@xframe_options_exempt
def xlsxV(request):
    # print("model: {}; access_token: {}".format(request.GET.get("model"), request.GET.get("access_token")))
    return render(request, 'WOPI/xlsx.html', {
        "model": request.GET.get("model"),
        "access_token": request.GET.get("access_token"),
        "host_web": 'http://' + SERVER_HOST
    })
