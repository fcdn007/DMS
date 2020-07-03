import datetime
import re

import numpy as np
import pandas as pd
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer_its


def get_queryset_base(model_, query_params_):
    query_params = {}
    tmp_dict = query_params_.dict()
    # print(">>>>>> model_ >>>>>")
    # pprint(model_)
    # print(">>>>>> query_params_ >>>>>")
    # pprint(query_params_)
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
    serializer = Serializer_its(settings.SECRET_KEY, 3600)
    info = {'confirm': num}
    token = serializer.dumps(info)  # bytes
    token = token.decode('utf8')  # 解码, str
    return token
