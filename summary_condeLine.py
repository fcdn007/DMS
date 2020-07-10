import subprocess
from collections import defaultdict

apps = ["databaseDemo", "ADVANCE", "BIS", "LIMS", "SEQ", "EMR", "USER", "PROJECT"]
line_counts = defaultdict(dict)
for app in apps:
    res1 = ""
    res2 = ""
    if app == "databaseDemo":
        # 计算后端代码
        backend_files = ["supervisord.ini", "README.md", "gunicorn.conf.py", "databaseDemo.conf", "bkdb.sh",
                          "db_pool/mysql/base.py"]
        backend_dirs = ["util/*", "databaseDemo/*"]
        res1 = subprocess.check_output("wc -l {} 2>/dev/null |tail -n1".format(" ".join(backend_files + backend_dirs)), shell=True)
        # 计算前端代码
        frontend_files = ["static/javascript/custom.js", "templates/base.html", "templates/single_page.html"]
        res2 = subprocess.check_output("wc -l {} 2>/dev/null |tail -n1".format(" ".join(frontend_files)), shell=True)

    else:
        res1 = subprocess.check_output("wc -l {}/* 2>/dev/null |tail -n1".format(app), shell=True)
        # 计算前端代码
        if app == "USER":
            frontend_files = ["templates/registration_base.html", "templates/{}/*".format(app),
                              "templates/registration/*"]
            res2 = subprocess.check_output("wc -l {} 2>/dev/null |tail -n1".format(" ".join(frontend_files)), shell=True)
        else:
            res2 = subprocess.check_output("wc -l templates/{}/* 2>/dev/null |tail -n1".format(app), shell=True)

    line_counts[app]["backend"] = int(str(res1).split()[1])
    try:
        line_counts[app]["frontend"] = int(str(res2).split()[1])
    except IndexError:
        line_counts[app]["frontend"] = 0

print("\t".join(["App", "backend", "frontend", "Total"]))
sum_count = [0]*2
for app in apps:
    print("{}\t{}\t{}\t{}".format(app, line_counts[app]["backend"], line_counts[app]["frontend"],
                                  line_counts[app]["backend"]+line_counts[app]["frontend"]))
    sum_count[0] += line_counts[app]["backend"]
    sum_count[1] += line_counts[app]["frontend"]
print("All\t{}\t{}\t{}".format(sum_count[0], sum_count[1], sum_count[0] + sum_count[1]))
