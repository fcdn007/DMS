from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from USER.models import UserInfo


# Create your views here.
@login_required
def HomeV(request):
    return render(request, 'base.html')


@login_required
def TestV(request, id):
    if request.method == 'POST':
        field1 = request.POST.get('methycaptureinfo')
        print(">>>>> request.POST:")
        pprint(request.POST)
        print(">>>>> field1:")
        print(field1)
    else:
        return render(request, 'Test/test.{}.html'.format(id))


@login_required
def UrlSearchV(request):
    all_urls = {}
    all_urls["首页"] = '/Home/'
    all_urls["网站概览"] = '/Home/'
    # 添加用户模块到all_urls
    all_urls["用户信息"] = '/USER/UserInfo/'
    all_urls["注册"] = '/USER/register/'
    all_urls["退出登录"] = '/accounts/logout/'
    all_urls["修改密码"] = '/accounts/password_change/'
    all_urls["忘记密码"] = '/accounts/password_reset/'
    # 根据用户权限添加可用url到all_urls
    user = UserInfo.objects.get(username=request.user.username)
    for perm in list(user.get_all_permissions()):
        app, tmp_str = perm.split(".")
        perm_part1, perm_part2 = tmp_str.split("_")[0:2]
        if app in ["BIS", "LIMS", "SEQ", "EMR"] and perm_part1 == "view":
            model2title = {
                "sampleinventoryinfo": ["SampleInventoryInfo", "样本库信息管理 样本库存信息"],
                "sampleinfo": ["SampleInfo", "样本库信息管理 样本信息"],
                "extractinfo": ["ExtractInfo", "样本库信息管理 核酸提取信息"],
                "dnausagerecordinfo": ["DNAUsageRecordInfo", "样本库信息管理 核酸使用记录信息"],
                "methylibraryinfo": ["Methy/MethyLibraryInfo", "实验项目信息管理 甲基化检测 甲基化建库信息"],
                "methycaptureinfo": ["Methy/MethyCaptureInfo", "实验项目信息管理 甲基化检测 捕获文库信息"],
                "methypoolinginfo": ["Methy/MethyPoolingInfo", "实验项目信息管理 甲基化检测 pooling映射信息"],
                "sequencinginfo": ["SequencingInfo", "分析结果管理 测序上机信息"],
                "methyqcinfo": ["QC/MethyQCInfo", "分析结果管理 QC信息 甲基化检测"],
                "clinicalinfo": ["ClinicalInfo", "病历信息管理 临床信息概述"],
                "liverpathologicalinfo": ["Pathology/LiverPathologicalInfo", "病历信息管理 病理报告信息 肝癌"],
                "tmdinfo": ["Test/TMDInfo", "病历信息管理 医院检查项目信息 肿瘤标志物检测"],
                "biocheminfo": ["Test/BiochemInfo", "病历信息管理 医院检查项目信息 生化检测"],
                "followupinfo": ["FollowupInfo", "病历信息管理 随访信息"]
            }
            all_urls[model2title[perm_part2][1]] = '/{}/{}/'.format(app, model2title[perm_part2][0])

        elif app == "ADVANCE" and tmp_str == "access_Advance":
            all_urls["高级功能 高级搜索"] = '/{}/AdvanceSearch/'.format(app)
            all_urls["高级功能 订制上传"] = '/{}/AdvanceUpload/'.format(app)

    print(">>>>>>>> all_urls: {}".format(all_urls))
    query_str = request.GET.get('query_str', None)
    if query_str is None:
        return JsonResponse([])
    res = []
    # 根据name返回res列表
    for ref_str in list(all_urls.keys()):
        if ref_str.find(query_str.strip()) != -1:
            res.append({ref_str: all_urls[ref_str]})
    print(">>>>>>>> res: {}".format(res))
    return JsonResponse({"res": res})

