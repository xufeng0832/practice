#!/usr/bin/env python3
#Created by xuchao on 16/7/4.
'''
状态码:

200  登录成功
201  上传文件成功
202  可以上传
203  注册成功
204  文件准备接受文件
205  目录切换成功
206  执行pwd

300  账号已存在 注册失败
301  账号或密码错误

400  上传文件失败
401  空间不足
403  文件不存在
404  没有这么目录
405  命令输入错误
'''

import socketserver
import json,os,hashlib,sys
import subprocess,platform
from modules.utility import *
class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            data = self.request.recv(1024)
            if not data:return
            task_data = json.loads(data.decode())
            task_what = task_data.get("What")
            if hasattr(self, "task_%s" % task_what):
                func = getattr(self, "task_%s" % task_what)
                user = func(task_data)
                if user:
                    self.task_cmd(user)

    # 登录后执行命令
    def task_cmd(self,use):
        """

        :param use:
        :return:
        """
        self.Root_Path = '../db/%s/'%use
        self.path = self.Root_Path

        while True:
            data = self.request.recv(1024)
            if not data:return
            task_data = json.loads(data.decode())
            task_action = task_data.get("action")
            if hasattr(self, "task_%s" % task_action):
                func = getattr(self, "task_%s" % task_action)
                func(task_data)
            else:
                re_msg = {'Status':405}
                re_msg = json.dumps(re_msg)
                self.request.send(bytes(re_msg, encoding='utf8'))

    # 读取密码文件
    def read_file(self):
        with open('../db/%s.pwd'%self.username,'r') as f:
            user_info = json.load(f)
            return user_info

    # 保存密码文件
    def wirt_file(self,args):
        with open('../db/%s.pwd' % self.username,'w') as f:
            json.dump(args,f)

    # 下载
    def task_get(self,args):
        print(args)
        filename = args.get('filename')
        abs_filepath = self.path+filename
        if os.path.isfile(abs_filepath):
            file_Md5 = md5sum(abs_filepath)
            file_size = os.stat(abs_filepath).st_size
            filename = Spit(abs_filepath)[-1]
            print('file:%s size:%s' % (abs_filepath, file_size))
            msg_data = {"status": 204,
                        "filename": filename,
                        "file_size": file_size,
                        "file_md5":file_Md5}
            self.request.send(bytes(json.dumps(msg_data), encoding="utf-8"))
            client_msg = self.request.recv(1024)
            if not client_msg:return
            confirm_data = json.loads(client_msg.decode())
            if confirm_data['status'] == 202:
                print(" 开始下载文件", filename)
                f = open(abs_filepath, 'rb')
                for line in f:
                    self.request.send(line)
                rest = self.request.recv(1024)
                rest_status = json.loads(rest.decode())
                if rest_status.get('status') == 201:
                    print(" 上传文件成功 ")
                elif rest_status.get('status') == 400:
                    print(" 文件未完整上传")
                else:print('???')
            elif confirm_data['status'] == 401:
                print('存储空间不足')
        else:
            msg_data = {"status":403}
            self.request.send(bytes(json.dumps(msg_data), encoding="utf-8"))

    # 上传
    def task_put(self, *args, **kwargs):
        # print("---put", args, kwargs)
        filename = args[0].get('filename')
        filesize = args[0].get('file_size')
        filemd5 = args[0].get('file_md5')
        u_info = self.read_file()
        Max = u_info.get('Max_space')
        use = u_info.get('use_space')
        # 判断 剩余空间>文件大小
        if Max - use > filesize:
            if u_info.get('%s%s'%(self.path,filename)):
                f=open('%s%s'%(self.path,filename),'ab')
                recv_size = u_info.get('%s%s'%(self.path,filename))
                server_response = {"status": 202,'point':recv_size}
                print('断点续传了')
            else:
                f = open('%s%s'%(self.path,filename),'wb')
                recv_size = 0
                server_response = {"status": 202}
            self.request.send(bytes(json.dumps(server_response), encoding='utf-8'))
            while recv_size < filesize:
                data = self.request.recv(4096)
                if not data:
                    f.close()
                    return
                f.write(data)
                recv_size += len(data)
                u_info['%s%s'%(self.path,filename)]=recv_size
                u_info['use_space']+=recv_size
                self.wirt_file(u_info)
                view_bar(recv_size, filesize)
            f.close()
            # 校验文件
            local_file_md5 = md5sum('%s%s' % (self.path, filename))
            if local_file_md5 == filemd5:
                self.request.send(bytes(json.dumps({"status": 201}), encoding='utf8'))
                del u_info['%s%s'%(self.path,filename)]
                self.wirt_file(u_info)
                print(' 上传成功')
            else:
                self.request.send(bytes(json.dumps({"status": 400}), encoding='utf8'))
                print(' 上传失败')
        else:
            server_response = {"status": 401}
            self.request.send(bytes(json.dumps(server_response), encoding='utf-8'))

    # cd 命令
    def task_cd(self,args):
        path = args.get('path')
        if path:
            if os.path.exists(self.Root_Path+path) and not path.startswith('../'):
                # 当前位置
                self.path = self.Root_Path+path
                re_msg = {'Status':205}
            else:
                re_msg = {'Status': 404}
            re_msg=json.dumps(re_msg)
        else:
            self.path = self.Root_Path
            re_msg = {'Status': 205}
            re_msg = json.dumps(re_msg)
        self.request.send(bytes(re_msg, encoding='utf8'))

    # 查看
    def task_ls(self,args):
        path = args.get('path')
        if path:
            if os.path.exists(self.Root_Path + path) and not path.startswith('../'):
                # 当前位置
                p = subprocess.Popen('ls -l %s%s'%(self.Root_Path,path), shell=True, stdout=subprocess.PIPE)
                rest = p.stdout.read()
                re_msg = {'Status': 205,'msg':str(rest,encoding='utf8')}
            else:
                re_msg = {'Status': 404}

        else:
            p = subprocess.Popen('ls -l %s'%self.path, shell=True, stdout=subprocess.PIPE)
            rest = p.stdout.read()
            re_msg = {'Status': 205, 'msg': str(rest,encoding='utf8')}

        # 解决粘包问题
        ready_tag = 'Ready|%s' % len(re_msg)
        self.request.send(bytes(ready_tag, encoding='utf8'))  # 发送数据长度
        feedback = self.request.recv(1024)  # 接收确认信息
        feedback = str(feedback, encoding='utf8')

        if feedback.startswith('Start'):
            # 发送命令的执行结果
            re_msg = json.dumps(re_msg)
            self.request.send(bytes(re_msg, encoding='utf8'))

    # 注册
    def task_Register(self,data):
        dir_path = '../db/%s'%data.get('username')
        if os.path.exists(dir_path):
            Re_data = {'Status':300}
        else:
            subprocess.run('mkdir %s'%dir_path, shell=True, check=True)
            # 限50M  52428800
            pwd_msg ={'username':data.get('username'),
                      'password':data.get('password'),
                      'Max_space':data.get('Max_space'),
                      'use_space':0
                      }
            with open('%s.pwd'%dir_path,'w') as f:
                json.dump(pwd_msg,f)
            Re_data = {'Status':203}
        Re_data=json.dumps(Re_data)
        self.request.send(bytes(Re_data,'utf8'))
    # 登录
    def task_Login(self,data):
        dir_path = '../db/%s' % data.get('username')
        if os.path.exists(dir_path):
            with open('%s.pwd' % dir_path, 'r') as f:
                pwd_msg=json.load(f)
            if data.get('password') == pwd_msg.get('password'):
                Re_data = {'Status':200}
            else:
                Re_data = {'Status': 301}
        else:
            Re_data = {'Status':301}
        Re_data_msg = json.dumps(Re_data)
        self.request.send(bytes(Re_data_msg,'utf8'))
        if Re_data.get('Status')==200:
            self.username = data.get('username')
            return data.get('username')
        else:return None