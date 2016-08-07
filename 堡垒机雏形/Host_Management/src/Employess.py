#!/usr/bin/env python3
#Created by xuchao on 16/8/3.
def Employees_interface(user):
    """
    普通用户界面
    :param user:
    :return:
    """
    while True:
        user_info = user.group
        host_all = []
        num = input('''
        1. 查看所属组
        2. 登陆主机
        0. 退出


-->:''')
        if num == '1':
            for i in user_info:
                print(i.Name)

        elif num == '2':
            flag = 1
            for i in user_info:
                for v in i.host:
                    print(flag,v.Host_Name)
                    flag+=1
                    host_all.append(v)
            print('0 返回')
            choose_host = input('选择登陆的主机:')
            if  choose_host.isdigit() and 0 < int(choose_host) <= len(host_all):
                User2Host = host_all[int(choose_host)-1]
                user_name = User2Host.UserName
                pass_word = User2Host.PassWord
                host_ip = User2Host.IP_addr
                host_port = User2Host.Port
                from src.Login_to_remote_host import run
                run(user.UserName,user_name,pass_word,host_ip,host_port)
                # print(user_name, pass_word, host_ip, host_port)
                '''
                登陆主机
                '''
            elif choose_host.isdigit() and choose_host == 0:
                continue
            else:
                print('请输入正确的主机')
        elif num == '0':
            break