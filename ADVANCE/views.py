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

from BIS.models import ExtractInfo
from USER.models import UserInfo, DatabaseRecord
from databaseDemo.settings import BASE_DIR, MEDIA_ROOT
from databaseDemo.tasks import make_new_merge_df_partly_by_celery, add_modelViewRecord_by_celery
from util.merge_df import apps_models_index, FOREIGNKEY_CONVERSION, FILECOLUMN_TO_FIELD
from util.merge_df import models_set, models_set2, FILECOLUMN_FOREIGNKEY_TO_MODEL, KEY1_TO_MODEL, apps
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
    merge_df_json = ""
    flag_update_list, time2_list, json_files_list = check_new_merge_df_all()
    wait_update = []
    time_stamp = 0
    for i in range(len(flag_update_list)):
        if time2_list[i] > time_stamp:
            time_stamp = time2_list[i]

        if flag_update_list[i]:
            wait_update.append(i)
            make_new_merge_df_partly_by_celery.delay(json_files_list[i], time2_list[i], i)
    merge_df_json = os.path.join(MEDIA_ROOT, "json", '{}.ALL.merge_df.json'.format(time_stamp))
    # print(">>>> merge_df_json: {}".format(merge_df_json))
    if len(wait_update) == 0:
        print("read merge_df.json")
    else:
        print("rebuild merge_df.json")

    if request.method == 'POST':
        post_models_index = [int(x) for x in request.POST['model_index'].split(', ')]
        print("post_models_index: {}".format(post_models_index))
        res_filtered = ""
        res_raw_len = 0
        # 判断单表查询, 单模块查询还是跨模块查询
        if len(post_models_index) == 1:
            model_str = models_set2[int(post_models_index[0])]
            objs = models_set[int(post_models_index[0])].objects
            res_raw = objs.all()
            res_raw_len = objs.count()
            normal_fields = ['id', 'last_modify_time', 'create_time'] + \
                            list(FILECOLUMN_TO_FIELD['normal'][model_str].values())
            if model_str in FILECOLUMN_TO_FIELD['normalAdd']:
                normal_fields = normal_fields + [x[0] for x in FILECOLUMN_TO_FIELD['normalAdd'][model_str].values()]
            foreign_fields = []
            if model_str in FILECOLUMN_TO_FIELD['foreign']:
                for foreign_key in list(FILECOLUMN_TO_FIELD['foreign'][model_str].values()):
                    foreign_fields.append(FOREIGNKEY_CONVERSION[foreign_key] + "__" + foreign_key)
                if model_str in FILECOLUMN_TO_FIELD['foreignAdd']:
                    for foreign_key in [x[4] for x in FILECOLUMN_TO_FIELD['foreignAdd'][model_str].values()]:
                        foreign_fields.append(FOREIGNKEY_CONVERSION[foreign_key] + "__" + foreign_key)
            if request.POST['queryset']:  # 有过滤条件
                # (0  ClinicalInfo  hospital  exact  hosp1) AND (0  ClinicalInfo  gender  exact  男) 等于(大小写严格匹配)
                # (0  ClinicalInfo  age  iexact  20) 等于(忽略大小写)
                # (0  ClinicalInfo  name  contains  李) 包含(大小写严格匹配)
                # (0  ClinicalInfo  age  icontains  李) 包含(忽略大小写)
                # (0  ClinicalInfo  age  gt  30) 大于
                # (0  ClinicalInfo  age  gte  30) 大于等于
                # (0  ClinicalInfo  age  lt  30) 小于
                # (0    ClinicalInfo    age lte  30) 小于等于
                for query in request.POST['queryset'].split("\n"):
                    conditionite = iter(query.split(" AND "))
                    while True:
                        try:
                            currentcondition = next(conditionite)
                            not_, m, f, vp, v = currentcondition.split("\t")
                            if f not in FILECOLUMN_TO_FIELD['normal'][m].values() and \
                                    f not in [x[0] for x in FILECOLUMN_TO_FIELD['normalAdd'][m].values()]:
                                f = FOREIGNKEY_CONVERSION[f] + "__" + f
                            not_ = int(not_[1:])
                            print("not_:{}".format(not_))
                            v = v[:-1]
                            currentparam = {f + "__" + vp: v}
                            print("currentparam: {}".format(currentparam))
                            if not_ == 1:
                                res_raw = res_raw.exclude(**currentparam)
                            elif not_ == 0:
                                res_raw = res_raw.filter(**currentparam)
                            else:
                                raise ValueError
                        except StopIteration:
                            pass
                        finally:
                            break
            else:
                res_raw = objs.all()
            if len(res_raw) > 0:
                tmp_dict = pd.DataFrame(list(res_raw.values(*normal_fields)))
                if len(foreign_fields) > 0:
                    old_col_names = [x for x in foreign_fields]
                    foreign_keys = ['id'] + foreign_fields
                    tmp_dict2 = pd.DataFrame(list(res_raw.values(*foreign_keys)))
                    if model_str == 'SequencingInfo':
                        tmp_dict2_shift = tmp_dict2.groupby(['id'])
                        tmp_dict3 = {}
                        for tmp_id, tmp_group in tmp_dict2_shift:
                            tmp_dict3[tmp_id] = {}
                            for tmp_col in tmp_group.columns:
                                if tmp_col == 'id':
                                    tmp_dict3[tmp_id]['id'] = tmp_id
                                    continue
                                tmp_values = [' ' if x is None else str(x) for x in
                                              tmp_group.loc[:, tmp_col]]
                                if len(tmp_values) > 1 and ' ' in tmp_values:
                                    tmp_values.remove(' ')
                                tmp_dict3[tmp_id][tmp_col] = ', '.join(tmp_values)
                        tmp_dict2 = pd.DataFrame.from_dict(tmp_dict3, orient='index')
                    rename_dict = {}
                    for col_name in old_col_names:
                        rename_dict[col_name] = col_name.split("__")[1]
                    tmp_dict2.rename(columns=rename_dict, inplace=True)
                    # print(">>>line 252 tmp_dict: {}".format(tmp_dict))
                    # print(">>>line 253 tmp_dict2: {}".format(tmp_dict2))
                    tmp_dict = pd.merge(tmp_dict, tmp_dict2, on='id')
                res_filtered = tmp_dict
                # print(">>>line 246 res_filtered: {}".format(res_filtered))
                if model_str == 'ExtractInfo':
                    res_filtered.loc[:, 'totalM'] = res_filtered.loc[:, 'dna_con'] * res_filtered.loc[:, 'dna_vol']
                    res_filtered.loc[:, 'remainM'] = res_filtered.loc[:, 'totalM'] - res_filtered.loc[:, 'successM'] - \
                                                     res_filtered.loc[:, 'failM'] - res_filtered.loc[:, 'researchM'] - \
                                                     res_filtered.loc[:, 'othersM']
                elif model_str == 'MethyLibraryInfo':
                    res_filtered.loc[:, 'dna_con'] = [ExtractInfo.objects.get(dna_id=x).dna_id for x in
                                                      res_filtered.loc[:, 'dna_id']]
            else:
                empty_dict = {}
                if model_str == 'ExtractInfo':
                    normal_fields = normal_fields + ['totalM', 'remainM']
                elif model_str == 'MethyLibraryInfo':
                    normal_fields = normal_fields + ['dna_con']
                for field in normal_fields:
                    empty_dict[field] = {}
                for field in foreign_fields:
                    empty_dict[field.split("__")[1]] = {}
                res_filtered = pd.DataFrame.from_dict(empty_dict, orient='index')
            old_col_names = list(res_filtered.columns)
            rename_dict = {}
            for col_name in old_col_names:
                if col_name not in FILECOLUMN_FOREIGNKEY_TO_MODEL:
                    rename_dict[col_name] = model_str + "__" + col_name
            res_filtered.rename(columns=rename_dict, inplace=True)
            # print(">>>line 275 res_filtered: {}".format(res_filtered))
        else:
            query_apps = {}
            for index_ in range(len(apps_models_index)):
                for query_index in post_models_index:
                    if query_index in apps_models_index[index_]:
                        query_apps[apps[index_]] = 1
            if len(query_apps.keys()) == 1:
                app = list(query_apps.keys())[0]
                app_index = apps.index(app)
                if app_index in wait_update:
                    sleep_n = 0
                    done_file = os.path.join(MEDIA_ROOT, "json", '{}.{}.rebuild_done.json'.format(time2_list[app_index],
                                                                                                  apps[app_index]))
                    while True:
                        print("sleep {}".format(5 * sleep_n))
                        if os.path.exists(done_file) or os.path.exists(merge_df_json):
                            break
                        else:
                            time.sleep(5)
                            sleep_n += 1
                merge_df = pd.read_json(json_files_list[app_index][time2_list[app_index]])
                print("read json_file: {}".format(json_files_list[app_index][time2_list[app_index]]))
            else:
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
                    # print("run make_new_merge_df_all in view")
                    make_new_merge_df_all(time2_list, json_files_list)

                if not os.path.exists(merge_df_json):
                    make_new_merge_df_all(time2_list, json_files_list)
                merge_df = pd.read_json(merge_df_json)
                print("read json_file: {}".format(merge_df_json))
            for col_ in list(merge_df.columns):
                if re.match(r'.+date$', col_) or re.match(r'.+time$', col_):
                    merge_df.loc[:, col_] = [datetime.datetime.strptime(date_, '%Y-%m-%dT%H:%M:%S.%fZ').date()
                                             if re.match(r'\d+-\d+-\d+T\d+:\d+:\d+\.\d+Z', str(date_))
                                             else datetime.datetime.strptime('2000-01-01', '%Y-%m-%d').date() for
                                             date_
                                             in merge_df.loc[:, col_]]
            merge_df_columns = list(merge_df.columns)
            model_cols = defaultdict(list)
            for col_ in merge_df_columns:
                parts = col_.split("__")
                if len(parts) > 1:
                    model_cols["join_keys"].append(col_)
                else:
                    model_cols[parts[0]].append(col_)
            post_models = [models_set2[x] for x in post_models_index]
            # 根据post_models提取merge_df
            cols_filtered = get_merge_df_cols(post_models)["id"]
            res_raw = merge_df.loc[:, cols_filtered].drop_duplicates()
            res_raw_len = res_raw.shape[0]
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
                                                                                        list(
                                                                                            FILECOLUMN_FOREIGNKEY_TO_MODEL.keys()) else \
                            condition_filter(res_raw, m + '__' + f, vp, v, not_)
                        filter_line = filter_line & filter_condition
                    filter_total = filter_line if filter_total == "" else filter_total | filter_line
                res_filtered = res_raw[filter_total]
        # make res_pro
        res_pro = res_filtered.to_dict('records')
        result = {
            'draw': 1,
            'recordsTotal': res_raw_len,
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
