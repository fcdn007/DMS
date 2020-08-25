import datetime
import os
import re
import time

import numpy as np
import pandas as pd
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer_its

from BIS.serializers import SampleInventoryInfoSerializer, SampleInfoSerializer, ExtractInfoSerializer, \
    DNAUsageRecordInfoSerializer
from EMR.serializers import ClinicalInfoSerializer, FollowupInfoSerializer, LiverPathologicalInfoSerializer, \
    TMDInfoSerializer, BiochemInfoSerializer
from LIMS.serializers import MethyLibraryInfoSerializer, MethyCaptureInfoSerializer, MethyPoolingInfoSerializer
from SEQ.serializers import SequencingInfoSerializer, MethyQCInfoSerializer
from databaseDemo.settings import MEDIA_ROOT, SECRET_KEY
from databaseDemo.tasks import add_modelViewRecord_by_celery
from util.merge_df import FILECOLUMN_FOREIGNKEY_TO_MODEL, models_set, models_set2

serializers_set = [SampleInventoryInfoSerializer, SampleInfoSerializer, ExtractInfoSerializer,
                   DNAUsageRecordInfoSerializer, MethyLibraryInfoSerializer, MethyCaptureInfoSerializer,
                   MethyPoolingInfoSerializer, SequencingInfoSerializer, MethyQCInfoSerializer, ClinicalInfoSerializer,
                   FollowupInfoSerializer, LiverPathologicalInfoSerializer, TMDInfoSerializer, BiochemInfoSerializer]


def get_queryset_base(model_, query_params_):
    query_params = {}
    tmp_dict = query_params_.dict()
    if 'format' in tmp_dict and tmp_dict['format'] == 'datatables':
        return model_.objects.all()
    for key_ in tmp_dict:
        if key_ == 'format' or key_ == 'fields':
            continue
        else:
            query_params[key_] = tmp_dict[key_]
    queryset = {}
    if len(query_params.keys()) > 0:
        queryset = model_.objects.filter(**query_params)
    else:
        queryset = model_.objects.all()
    return queryset


def read_file_by_stream(file_path, chunk_size=512):
    # print("readFile " + file_path)
    with open(file_path, "rb") as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def numeric_filter(value_series, d, vp):
    filter_ = [True] * len(value_series)
    if vp == 'gt':
        filter_ = value_series > d
    elif vp == 'gte':
        filter_ = value_series >= d
    elif vp == 'lt':
        filter_ = value_series < d
    elif vp == 'lte':
        filter_ = value_series <= d
    elif vp == 'exact':
        filter_ = value_series == d

    return filter_


def condition_filter(df, f, vp, v, not_):
    filter_ = [True] * len(df)
    if isinstance(df[f][0], str):
        if vp == 'exact':
            filter_ = df[f] == v
        elif vp == 'iexact':
            filter_ = [True if re.match(
                v, str(i), flags=re.IGNORECASE) else False for i in list(df[f])]
        elif vp == 'contains':
            filter_ = [True if re.search(
                v, str(i)) else False for i in list(df[f])]
        elif vp == 'icontains':
            filter_ = [True if re.search(
                v, str(i), flags=re.IGNORECASE) else False for i in list(df[f])]
        else:
            filter_ = [True] * len(df)
    elif isinstance(df[f][0], datetime.date):
        d = datetime.date(2000, 1, 1)
        m1 = re.search(r'(\d{4}).(\d{1,2}).(\d{1,2})', v)
        m2 = re.search(r'(\d{1,2}).(\d{1,2}).(\d{4})', v)
        if re.match(r'\d{8}', v):
            d = datetime.date(int(v[:4]), int(v[4:6]), int(v[6:8]))
        elif m1:
            d = datetime.date(int(m1.group(1)), int(m1.group(2)), int(m1.group(3)))
        elif m2:
            d = datetime.date(int(m2.group(3)), int(m2.group(2)), int(m2.group(1)))
        filter_ = numeric_filter(df[f], d, vp)
    elif isinstance(df[f][0], np.floating) or isinstance(df[f][0], np.integer):
        v = float(v)
        filter_ = numeric_filter(df[f], v, vp)
    else:
        pass
    if int(not_) == 1:
        filter_ = [False if x else True for x in filter_]
    # print(">>>>>>>>>>>>> filter >>>>>>>>>>>")
    # pprint(filter_)
    return pd.Series(data=filter_)


def custom_token_generator(num):
    # 加密用户的身份信息，生成激活token
    serializer = Serializer_its(SECRET_KEY, 3600)
    info = {'confirm': num}
    token = serializer.dumps(info)  # bytes
    token = token.decode('utf8')  # 解码, str
    return token


def output_model_all_records(file_name0, data, col_name, file_ext, drop_cols=None):
    if drop_cols is None:
        drop_cols = ["id"]
    else:
        drop_cols = ["id"] + drop_cols

    ticks = time.time()
    res_df = pd.DataFrame(data)
    col_list = list(res_df.columns)
    res_df.loc[:, "索引"] = [x + 1 for x in range(res_df.shape[0])]
    res_df = res_df.loc[:, ["索引"] + [x for x in col_list if x not in drop_cols]]
    res_df.columns = ["索引"] + col_name
    if file_ext == "csv":
        file_name = "{}.all.csv".format(file_name0)
        file_path = os.path.join(MEDIA_ROOT, "csv", "{}.{}".format(ticks, file_name))
        doing_flag = file_path + '.doing'
        if os.path.exists(doing_flag):
            await_flag = True
            while await_flag:
                time.sleep(5)
                await_flag = os.path.exists(doing_flag)
        else:
            os.system("touch " + doing_flag)
            res_df.to_csv(file_path, index=False)
            os.system("rm " + doing_flag)

        response = StreamingHttpResponse(read_file_by_stream(file_path))
        response['Content-Type'] = 'application/octet-steam'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    elif file_ext == "xlsx":
        run_make_bool = False
        model_objects = models_set[models_set2.index(file_name0)].objects
        model_len = model_objects.count()
        model_last_modify_time = int(
            model_objects.values_list("last_modify_time").distinct().order_by("-last_modify_time")[0][0].strftime(
                "%Y%m%d%H%M%S%f"))
        last_info_file = os.path.join(MEDIA_ROOT, "xlsx", "mysql", "all_{}.latest.info.csv".format(file_name0))
        if not os.path.exists(last_info_file):
            run_make_bool = True
        else:
            last_info_df = pd.read_csv(last_info_file, header=0, encoding='utf-8')
            if int(last_info_df['len'][0]) != model_len or int(last_info_df['last_modify_time'][0]) != model_last_modify_time:
                run_make_bool = True

        if run_make_bool:
            file_name = "all_{}.xlsx".format(file_name0)
            file_path = os.path.join(MEDIA_ROOT, "xlsx", "mysql", "{}".format(file_name))
            doing_flag = file_path + '.doing'
            if os.path.exists(doing_flag):
                await_flag = True
                while await_flag:
                    time.sleep(5)
                    await_flag = os.path.exists(doing_flag)
            else:
                os.system("touch " + doing_flag)
                res_df.to_excel(file_path, index=False)
                os.system("rm " + doing_flag)
            res_df_info = pd.DataFrame(data={'len': [model_len], 'last_modify_time': [model_last_modify_time]})
            res_df_info.to_csv(last_info_file, index=False)
        return "True"


def df_queryset_filter(data, queryset, model_str=None, merge_df_bool=False, return_class='dict'):
    raw_df = pd.DataFrame(data)
    # print(">>>raw_df :{}".format(raw_df))
    # print(">>>queryset :{}".format(queryset))
    res_filtered = raw_df
    filter_total = []
    for i in queryset.split('\n'):
        filter_line = pd.Series(data=[True] * raw_df.shape[0])
        for j in i.split(' AND '):
            not_, m, f, vp, v = j.split('\t')[0:5]
            not_ = int(not_[1:].strip())
            v = v[:-1].strip()
            filter_condition = pd.Series()
            if merge_df_bool:
                if f in list(FILECOLUMN_FOREIGNKEY_TO_MODEL.keys()):
                    filter_condition = condition_filter(raw_df, f, vp, v, not_)
                else:
                    filter_condition = condition_filter(raw_df, m + '__' + f, vp, v, not_)
            else:
                filter_condition = condition_filter(raw_df, f, vp, v, not_)
            filter_line = filter_line & filter_condition
        filter_total = filter_line if len(filter_total) == 0 else filter_total | filter_line

    filter_rows = []
    for row_idx in range(len(filter_total)):
        if filter_total[row_idx]:
            filter_rows.append(row_idx)
    res_filtered = raw_df.loc[filter_rows, :].reset_index(drop=True)
    if return_class == 'pd.df':
        return res_filtered
    else:
        # make res_pro
        if model_str is not None:
            res_filtered.to_excel(os.path.join(MEDIA_ROOT, "xlsx", "user", "queryset_{}.xlsx".format(model_str)),
                                  index=False)
        res_pro = res_filtered.to_dict('records')
        result = {
            'draw': 1,
            'recordsTotal': raw_df.shape[0],
            'recordsFiltered': len(res_pro),
            'data': res_pro
        }
        return result


def singleModelV(request_, idx, template_path, col_name, drop_cols=None):
    serializer = serializers_set[idx]
    model_instance = models_set[idx]
    model_str = models_set2[idx]
    add_modelViewRecord_by_celery(model_str, request_.user.username)
    output_all_bool = request_.GET.get('all', 0)
    output_all_format = request_.GET.get('format', 'csv')
    queryset = request_.POST.get('queryset', 0)
    if queryset:
        serializer = serializer(model_instance.objects.all(), many=True)
        last_queryset_res = df_queryset_filter(serializer.data, queryset, model_str="{}_{}".format(model_str,
                                                                                                   request_.user.id))
        return JsonResponse(last_queryset_res)
    elif output_all_bool:
        res_data = serializer(model_instance.objects.all(), many=True).data
        if output_all_format != 'csv':
            return JsonResponse({"done": output_model_all_records(model_str, res_data, col_name, output_all_format,
                                                                  drop_cols=drop_cols)})
        else:
            return output_model_all_records(model_str, res_data, col_name, "csv", drop_cols=drop_cols)
    else:
        return render(request_, template_path)
