#!/usr/bin/env python3
#Created by xuchao on 16/7/4.
import hashlib,sys,logging
import json,socket,platform
from conf.Ftpconf import *

# 生成MD5
def Out_md5(arg):
    m = hashlib.md5()
    m.update(bytes(arg,'utf8'))
    return m.hexdigest()

# 进度条
def view_bar(num,total):
    rate = num / total
    rate_num= int(rate * 100)
    r = '\r[%-10s]%d%%' % ('=' * rate_num,rate_num, )
    sys.stdout.write(r)
    sys.stdout.flush()

def md5sum(fname):
    # 计算文件的MD5值
    def read_chunks(fh):
        fh.seek(0)
        chunk = fh.read(8096)
        while chunk:
            yield chunk
            chunk = fh.read(8096)
        else: #最后要将游标放回文件开头
            fh.seek(0)
    m = hashlib.md5()
    with open(fname, "rb") as fh:
        for chunk in read_chunks(fh):
            m.update(chunk)
    #上传的文件缓存 或 已打开的文件流
    # for chunk in read_chunks(fname):
    #     m.update(chunk)
    return m.hexdigest()

# 登陆
def login(flg):
    while True:
        username = input(' 请输入账号:').strip()
        password = input(' 请输入密码:').strip()
        if username and password:
            userinfo = {'What':flg,'username':username,'password':Out_md5(password)}
            return json.dumps(userinfo)

# 客户端连接
def Connection():
    ip_port=(SERVER.get('IP'),SERVER.get('PORT'))
    s=socket.socket()
    s.connect(ip_port)
    return s
# 判断系统
def Spit(arg):
    if platform.system() == 'Windows':
        BASE_DIR = arg.split('\\')
    else:
        BASE_DIR = arg.split('/')
    return BASE_DIR

# 注册
def Register(flg):
    username = input(' 请输入账号:').strip()
    password = input(' 请输入密码:').strip()
    while True:
        disk_space = input(' 请输入可用空间大小(以字节为单位MB):')
        if disk_space.isdigit():
            disk = int(disk_space)*1024*1024
            break
        else:
            print(' 输入类型错误请重新输入')
    # What 做什么 Register 注册
    userinfo = {'What':flg,
                'username':username,
                'password':Out_md5(password),
                'Max_space':disk}
    return json.dumps(userinfo)

def log_output():
    # 设置log全局 生成的用户名
    logger = logging.getLogger('FTP')
    # 设置全局最大上限的日志等级
    logger.setLevel(logging.DEBUG)
    # 设置文件输出日志
    fh = logging.FileHandler(INFO_LOG_DATA_PATH,encoding='utf-8')
    # 设置文件日志输出等级
    fh.setLevel(logging.INFO)
    # 设置输出信息 <年月日 时分秒 - 用户名 - 等级 - 内容>
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # 注册输出内容 到文件 输出
    fh.setFormatter(formatter)
    # 注册文件输出
    logger.addHandler(fh)
    return logger