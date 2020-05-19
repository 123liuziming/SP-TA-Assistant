import requests
import shutil
import os
import random


# 指定打包的压缩包名字
homework_name = ""
# 指定云平台账号
userName = ""
# 云平台密码(是加密过的密码,可以自己登录的时候发个http请求看)
password = ""


def login(username, passwd, usertype="Student"):
    url = "https://cloud-beihangsoft-cn.e2.buaa.edu.cn/Security/Login"
    inf = {"username": username, "Passwd": passwd, "usertype": usertype}
    s = requests.session()
    r = requests.post(url, data=inf, allow_redirects=False)
    cookies = r.cookies
    r = requests.post(url, data=inf)
    if r.status_code == requests.codes.ok:
        print("login successfully")
    else:
        print("fail to login", r.status_code)
    return cookies


def download(expId, cookies, dst="./out"):
    print("downloading..................")
    os.system("rm -rf ./out/*")
    url = "https://cloud-beihangsoft-cn.e2.buaa.edu.cn/Teacher/downloadAllHomework"
    params = {"expId": expId}
    r = requests.get(url, params=params, cookies=cookies)
    with open(os.path.join(dst, "out.zip"), "wb") as f:
        f.write(r.content)
    print("download successfully")


def unzipAndClassify(homework_name):
    os.chdir("./out")
    # print(os.getcwd())
    os.system("unar -e GBK out.zip")
    TA_list = ["刘子明", "胡哲宇", "李楠", "岑少锋", "姜一铭"]
    for name in TA_list:
        if not os.path.isdir(os.path.abspath(name)):
            os.mkdir(name)
    os.remove("./out.zip")
    file_list = os.listdir("./out")
    length = len(file_list) - 1
    each_length = length // len(TA_list)
    remain = length - len(TA_list) * each_length
    shutil.move("./out/提交情况.txt", ".")
    file_list.remove("提交情况.txt")
    for i, to in enumerate(TA_list):
        idx = 0
        while idx < each_length and i * each_length + idx < length:
            file_move = file_list[i * each_length + idx]
            from_path = os.path.join("./out", file_move)
            shutil.move(from_path, to)
            idx += 1
    for i in range(remain):
        rand = random.randint(0, len(TA_list) - 1)
        from_path = os.path.join("./out", file_list[-i - 1])
        shutil.move(from_path, TA_list[rand])
    os.rmdir("./out")
    os.chdir("..")
    os.system("zip -r %s.zip ./out/*" % homework_name)


if __name__ == "__main__":
    cookies = login(userName, password)
    download(654, cookies)
    unzipAndClassify(homework_name)
