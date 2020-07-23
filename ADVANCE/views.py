import datetime
import os
import re
import time
from collections import defaultdict

import pandas as pd
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import FieldError
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from USER.models import UserInfo, DatabaseRecord
from databaseDemo.settings import BASE_DIR, MEDIA_ROOT
from databaseDemo.tasks import make_new_merge_df_partly_by_celery, add_modelViewRecord_by_celery
from util.merge_df import models_set2, FILECOLUMN_FOREIGNKEY_TO_MODEL, KEY1_TO_MODEL, apps
from util.merge_df import save_records, check_new_merge_df_all, get_merge_df_cols, make_new_merge_df_all
from util.utils import read_file_by_stream, condition_filter
from .forms import FileUploadModelForm


# Create your views here.
def uniqueV(request):
    foreign_keys = {
        'SampleInfo': ['sampler_id'],
        'ExtractInfo': ['sampler_id', 'sample_id'],
        'DNAUsageRecordInfo': ['sampler_id', 'dna_id'],
        'MethyLibraryInfo': ['sampler_id', 'dna_id'],
        'MethyPoolingInfo': ['sampler_id', 'singleLB_id', 'poolingLB_id'],
        'SequencingInfo': ['poolingLB_id'],
        'MethyQCInfo': ['sampler_id', 'singleLB_Pooling_id', 'sequencing_id'],
        'ClinicalInfo': ['sampler_id'],
        'FollowupInfo': ['sampler_id', 'clinical_id'],
        'LiverPathologicalInfo': ['sampler_id', 'clinical_id'],
        'LiverTMDInfo': ['sampler_id', 'clinical_id'],
        'LiverBiochemInfo': ['sampler_id', 'clinical_id']
    }
    data = {}
    key1 = request.GET['model']
    key2 = request.GET['filed']
    try:
        if key1 in foreign_keys and key2 in foreign_keys[key1]:
            data['values'] = [x[0] for x in FILECOLUMN_FOREIGNKEY_TO_MODEL[key2].objects.values_list(key2).distinct(
                              ).order_by(key2)]
        else:
            data['values'] = [x[0] for x in
                              KEY1_TO_MODEL[key1].objects.values_list(key2).distinct().order_by(key2)]
    except:
        data['values'] = []
    return JsonResponse(data)

@csrf_exempt
def uploadV(request):
    # pprint(request)
    if request.method == "POST":
        form = FileUploadModelForm(data=request.POST, files=request.FILES)
        user = UserInfo.objects.get(username=request.user.username)
        # print("form: %s" % form)

        if form.is_valid():
            # print("form.is_valid(): TRUE")
            upload_file = form.save()
            # print('upload_file.uploadUrl: %s' % upload_file.uploadUrl)
            # print('upload_file.uploadOperator: %s' % upload_file.uploadOperator)
            # print('upload_file.uploadFile: %s' % upload_file.uploadFile)
            # print(upload_file.uploadFile.path)
            # read file and add records to model
            total, valid, add, warning, error_msg, fatal_error = save_records(upload_file)
            if fatal_error:
                context2 = {
                    'userinfo': user, 'model_changed': request.POST.get('uploadUrl'),
                    'operation': "批量上传失败",
                    'memo': "file_path: {};fatal_error: {}".format(upload_file.uploadFile.path, fatal_error)
                }
                record_obj = DatabaseRecord(**context2)
                record_obj.save()
                return JsonResponse({
                    'error_msg_fatal': fatal_error
                })
            else:
                context2 = {
                    'userinfo': user, 'model_changed': request.POST.get('uploadUrl'),
                    'operation': "批量上传成功",
                    'memo': "file_path: {};all_records: {};valid_records: {};error_msg_tolerant: {}".format(
                        upload_file.uploadFile.path, total, valid, error_msg)
                }
                record_obj = DatabaseRecord(**context2)
                record_obj.save()
                return JsonResponse({
                    'all_records': total, 'valid_records': valid, 'add_records': add, 'warning': warning,
                    'error_msg_tolerant': error_msg
                })
        else:
            # print("form.is_valid(): FALSE")
            data = {'error_msg_fatal': "严重错误！！！文件上传和批量添加失败。只允许上传以下格式文件：txt, csv and xlsx。"}
            context2 = {
                'userinfo': user, 'model_changed': request.POST.get('uploadUrl'),
                'operation': "批量上传文件格式错误",
                'memo': "无"
            }
            record_obj = DatabaseRecord(**context2)
            record_obj.save()
            return JsonResponse(data)
    return JsonResponse({'error_msg_fatal': '严重错误！！！只接受POST请求。'})


@login_required
@never_cache
def AdvanceUploadV(request):
    add_modelViewRecord_by_celery("AdvanceUpload", request.user.username)
    return render(request, 'ADVANCE/AdvanceUpload.html')


@login_required
@permission_required('ADVANCE.access_Advance')
def AdvanceSearchV(request):
    # 合并所有model，形成一张大表
    # 检测所有model的最新修改时间time1，
    # > 如果time1等于已有json文件的时间戳time2，直接读取已有的json文件，
    # > 否则重新创建merge_df，并把merge_df输出为json文件，打上时间戳。清除旧的json文件(保留10个)
    merge_df = ""
    flag_update_list, time2_list, json_files_list = check_new_merge_df_all()
    wait_update = []
    time_stamp = 0
    for i in range(len(flag_update_list)):
        if time2_list[i] > time_stamp:
            time_stamp = time2_list[i]

        if flag_update_list[i]:
            wait_update.append(i)
            make_new_merge_df_partly_by_celery.delay(json_files_list[i], time2_list[i], i)

    if len(wait_update) == 0:
        print("read merge_df.json")
    else:
        print("rebuild merge_df.json")

    if request.method == 'POST':
        if len(wait_update) > 0:
            sleep_n = 0
            while len(wait_update) > 0:
                print("sleep {}".format(5 * sleep_n))
                for i in wait_update:
                    done_file = os.path.join(MEDIA_ROOT, "json", '{}.{}.rebuild_done.json'.format(time2_list[i],
                                                                                                  apps[i]))
                    if os.path.exists(done_file):
                        wait_update.remove(i)
                time.sleep(5)
                sleep_n += 1
            make_new_merge_df_all(time2_list, json_files_list)

        merge_df = pd.read_json(os.path.join(MEDIA_ROOT, "json", '{}.ALL.merge_df.json'.format(time_stamp)))
        for col_ in list(merge_df.columns):
            if re.match(r'.+date$', col_) or re.match(r'.+time$', col_):
                merge_df.loc[:, col_] = [datetime.datetime.strptime(date_, '%Y-%m-%dT%H:%M:%S.%fZ').date()
                                         if re.match(r'\d+-\d+-\d+T\d+:\d+:\d+\.\d+Z', str(date_))
                                         else datetime.datetime.strptime('2000-01-01', '%Y-%m-%d').date() for date_
                                         in merge_df.loc[:, col_]]
        merge_df_columns = list(merge_df.columns)
        model_cols = defaultdict(list)
        for col_ in merge_df_columns:
            parts = col_.split(".")
            if len(parts) > 1:
                model_cols["join_keys"].append(col_)
            else:
                model_cols[parts[0]].append(col_)
        post_models_index = request.POST['model_index'].split(', ')
        post_models = [models_set2[int(x)] for x in post_models_index]
        # 根据post_models提取merge_df
        cols_filtered = get_merge_df_cols(post_models)["id"]
        res_raw = merge_df.loc[:, cols_filtered].drop_duplicates()
        res_filtered = res_raw
        if request.POST['queryset']:  # 有过滤条件
            filter_total = ""
            for i in request.POST['queryset'].split('\n'):
                filter_line = pd.Series(data=[True] * res_raw.shape[0])
                for j in i.split(' AND '):
                    not_, m, f, vp, v = j.split('\t')
                    not_ = not_[1:]
                    v = v[:-1]
                    filter_condition = condition_filter(res_raw, f, vp, v, not_) if f in \
                                            list(FILECOLUMN_FOREIGNKEY_TO_MODEL.keys()) else \
                                            condition_filter(res_raw, m + '.' + f, vp, v, not_)
                    filter_line = filter_line & filter_condition
                filter_total = filter_line if filter_total == "" else filter_total | filter_line
            res_filtered = res_raw[filter_total]
        # make res_pro
        res_pro = res_filtered.to_dict('records')
        result = {
                'draw': 1,
                'recordsTotal': res_raw.shape[0],
                'recordsFiltered': len(res_pro),
                'data': res_pro
            }
        return JsonResponse(result)
    else:
        models_query_index = request.GET.get('models_query_index', None)
        if models_query_index is None:
            add_modelViewRecord_by_celery("AdvanceSearch", request.user.username)
            return render(request, 'ADVANCE/AdvanceSearch.html')
        else:
            models_query = [models_set2[int(x)] for x in models_query_index.split(', ')]
            cols_dict = get_merge_df_cols(models_query)
            return JsonResponse(cols_dict)


def Download_excel(request, name):
    # print(model)
    file_name = "{}.template.xlsx".format(name)
    file_path = os.path.join(BASE_DIR, "excelData", file_name)
    if not os.path.exists(file_path):
        return
    file_path = os.path.join(BASE_DIR, "excelData", file_name)
    response = StreamingHttpResponse(read_file_by_stream(file_path))
    response['Content-Type'] = 'application/octet-steam'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response


def plotDataV(request):
    data = {}
    data_sum = 0
    try:
        key1 = KEY1_TO_MODEL[request.GET['model']]
        key2 = request.GET['field']
        values = key1.objects.values_list(key2)
        data_sum = len(values)
        for v in values:
            if isinstance(v[0], str):
                data[v[0]] = data[v[0]] + 1 if v[0] in data else 1
            elif isinstance(v[0], int) or isinstance(v[0], float):
                k = v[0] // 10
                data[k] = data[k] + 1 if k in data else 1
            elif isinstance(v[0], datetime.date):
                k = int("{}01".format(v[0].year)) if v[0].month < 7 else int("{}02".format(v[0].year))
                data[k] = data[k] + 1 if k in data else 1

        for k in data:
            data[k] = round(100 * data[k] / data_sum, 2)
    except FieldError:
        data['空'] = 100

    data_sort = {}
    if isinstance(list(data.keys())[0], str):
        for k in sorted(data, key=lambda x: x):
            data_sort[k] = data[k]
    elif isinstance(list(data.keys())[0], int) or isinstance(list(data.keys())[0], float):
        if re.match(r'^\d{6}$', str(list(data.keys())[0])):
            for k in sorted(data, key=lambda x: x):
                k_str = "{}年上半年".format(str(k)[:4]) if str(k)[4:] == '01' else "{}年下半年".format(str(k)[:4])
                data_sort[k_str] = data[k]
        else:
            for k in sorted(data, key=lambda x: x):
                k_str = "{}~{}".format(int(10 * k), int(10 * (k + 1)))
                data_sort[k_str] = data[k]

    return JsonResponse({'sum': data_sum, 'data': data_sort})
