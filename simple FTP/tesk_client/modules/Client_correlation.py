#!/usr/bin/env python3
#Created by xuchao on 16/7/4.

import os
from modules.utility import *

class Myclient:
    def __init__(self):
        self.SK = Connection()
    def run(self):
        while True:
            chone = input('''
            1 注册
            2 登陆
            3 退出
请输入:''')
            if chone == '1':
                Send = Register('Register')
            elif chone == '2':
                Send = login('Login')
            elif chone == '3':
                self.SK.close()
                exit('bey~')
            else:continue
            self.SK.send(bytes(Send,encoding='utf8'))
            recv_data=self.SK.recv(1024)
            recv_dict=json.loads(str(recv_data,'utf8'))
            if recv_dict.get('Status') == 203:
                print(' 注册成功 ')
            elif recv_dict.get('Status') == 300:
                print(' 账户已存在')
            elif recv_dict.get('Status') == 301:
                print(' 账号密码错误')
            elif recv_dict.get('Status') == 200:
                while True:
                    data_msg = input('>>>:').strip()
                    if len(data_msg) == 0: continue
                    if data_msg == 'exit':
                        self.SK.close()
                        exit('bey~')
                    cmd_list = data_msg.split()
                    task_type = cmd_list[0]
                    if task_type == 'put' and len(cmd_list) > 1:
                        self.task_put(cmd_list)
                    elif task_type == 'cd':
                        self.task_cd(cmd_list)
                    elif task_type == 'ls':
                        self.task_ls(cmd_list)
                    elif task_type == 'get' and len(cmd_list) > 1:
                        self.task_get(cmd_list)
                    else:
                        print("不支持的任务类型", task_type)
                        continue
        self.SK.close()
    # 查看
    def task_ls(self,cmd_list):
        if len(cmd_list) > 1:
            msg_data = {"action": cmd_list[0],
                        "path": cmd_list[1],
                        }
        else:
            msg_data = {"action": cmd_list[0]}
        self.SK.send(bytes(json.dumps(msg_data), encoding="utf-8"))

        ready_tag = self.SK.recv(1024)  # 收取带数据长度的字节：Ready|9998
        ready_tag = str(ready_tag, encoding='utf8')
        if ready_tag.startswith('Ready'):  # Ready|9998
            msg_size = int(ready_tag.split('|')[-1])  # 获取待接收数据长度
            start_tag = 'Start'
            self.SK.send(bytes(start_tag, encoding='utf8'))  # 发送确认信息

            # 基于已经收到的待接收数据长度，循环接收数据
            recv_size = 0
            recv_msg = b''
            while recv_size < msg_size:
                recv_data = self.SK.recv(1024)
                recv_msg += recv_data
                recv_size += len(recv_data)
                print('MSG SIZE %s RECE SIZE %s' % (msg_size, recv_size))


            # rest = self.SK.recv(1024)
            rest_msg = json.loads(recv_msg.decode())
            if rest_msg.get('Status') == 404:
                print(' 路径错误')
            elif rest_msg.get('Status') == 205:
                print(rest_msg.get('msg'))

    # 切换目录
    def task_cd(self,cmd_list):
        if len(cmd_list) > 1:
            msg_data = {"action": cmd_list[0],
                        "path": cmd_list[1],
                        }
        else:
            msg_data = {"action": cmd_list[0]}
        self.SK.send(bytes(json.dumps(msg_data), encoding="utf-8"))

        rest = self.SK.recv(1024)
        rest_msg = json.loads(rest.decode())
        if rest_msg.get('Status') == 205:
            print(' 目录切换完成')
        elif rest_msg.get('Status') == 404:
            print(' 该目录不存在')
    # 下载
    def task_get(self, cmd_list):
        msg_data = {"action": cmd_list[0],
                    "filename": cmd_list[1],
                    }
        self.SK.send(bytes(json.dumps(msg_data), encoding="utf-8"))
        rest = self.SK.recv(1024)
        rest_info = json.loads(rest.decode())
        if rest_info.get('status') == 204:
            filename = rest_info.get('filename')
            filesize = rest_info.get('file_size')
            filemd5 = rest_info.get('file_md5')
            server_response = {"status": 202}
            self.SK.send(bytes(json.dumps(server_response), encoding='utf-8'))
            with open('./%s' %filename, 'wb') as f:
                recv_size = 0
                while recv_size < filesize:
                    data = self.SK.recv(4096)
                    f.write(data)
                    recv_size += len(data)
                    # print('filesize: %s  recvsize:%s' % (filesize, recv_size))
                    view_bar(recv_size,filesize)

            local_file_md5 = md5sum('./%s' %filename)
            if local_file_md5 == filemd5:
                client_status = {"status": 201}
                print('%s 文件下载成功'%filename)
            else:
                client_status = {"status": 400}
                print('%s 下载失败'%filename)
            self.SK.send(bytes(json.dumps(client_status), encoding='utf-8'))
        elif rest_info.get('status') == 403:
            print(' 这个文件不存在')

    # 上传
    def task_put(self,arg):
        """
        :param arg: 传入参数
        :return:
        """
        abs_filepath = arg[1]
        if os.path.isfile(abs_filepath):   #路径是否存在
            file_Md5 = md5sum(abs_filepath)
            file_size = os.stat(abs_filepath).st_size
            filename = Spit(abs_filepath)[-1]
            print('file:%s size:%s' % (abs_filepath, file_size))
            msg_data = {"action": "put",
                        "filename": filename,
                        "file_size": file_size,
                        "file_md5":file_Md5}

            self.SK.send(bytes(json.dumps(msg_data), encoding="utf-8"))
            server_confirmation_msg = self.SK.recv(1024)
            confirm_data = json.loads(server_confirmation_msg.decode())
            if confirm_data['status'] == 202:
                print(" 开始上传文件", filename)
                f = open(abs_filepath, 'rb')
                if confirm_data.get('point'):    #判断是否有断点
                    f.seek(confirm_data.get('point'))
                    print(' 继续断点开始上传')
                for line in f:
                    self.SK.send(line)

                rest = self.SK.recv(1024)
                rest_status = json.loads(rest.decode())
                if rest_status.get('status') == 201:
                    print(" 上传文件成功 ")
                elif rest_status.get('status') == 400:
                    print(" 文件未完整上传")
            elif confirm_data['status'] == 401:
                print('存储空间不足')

        else:
            print("\033[31;1mfile [%s] is not exist\033[0m" % abs_filepath)
