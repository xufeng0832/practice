#!/usr/bin/env python3
#Created by xuchao on 16/8/2.
from lib.sql_related import *


def administrator_interface(user):
    """
    管理员用户界面
    :param user:
    :return:
    """
    while True:
        select_ = Sql_query()
        sql_add = Sql_Add_table()
        num = input('''
    1. 添加用户
    2. 添加组
    3. 添加主机
    4. 查看所有用户
    5. 查看所有组
    6. 查看所有主机信息
    7. 将用户添加到组
    8. 将主机添加到组
    0. 退出
-->:''')

        if num == '1':
            username = input('账号:')
            password = input('密码:')
            sql_add.User_add(username,password)
        elif num == '2':
            name = input('组名:')
            sql_add.group_add(name)
        elif num == '3':
            host_name = input('host:')
            Ip = input('IP:')
            port = int(input('port:'))
            username = input('username:')
            password = input('password:')

            sql_add.Host_add(name=host_name, ip=Ip, port=port, username=username, password=password)
        elif num == '4':
            u = select_.select_User_all()
            for i in u:
                print(i.UserName)
        elif num == '5':
            g = select_.select_Group_all()
            for i in g:
                print(i.Name)
        elif num == '6':
            h = select_.select_Host_all()
            for i in h:
                print('主机名:%s   IP:%s   端口:%s' %(i.Host_Name,i.IP_addr,i.Port))
        elif num == '7':
            u2g_user = input('用户:')
            u2g_group = input('组:')
            sql_user = select_.select_User(u2g_user)
            sql_group = select_.select_Group(u2g_group)
            if sql_user and sql_group:
                sql_add.UserToGroup_add(sql_user, sql_group,)
            else:print('用户或组不存在:')

        elif num == '8':
            h2g_host = input('主机:')
            h2g_group = input('组:')
            sql_host = select_.select_Host(h2g_host)
            sql_group = select_.select_Group(h2g_group)
            if sql_host and sql_group:
                sql_add.HostToGroup_add(sql_host, sql_group,)
                # print(sql_group.ID,sql_host.ID)
            else:print('用户或组不存在:')
        elif num == '0':
            break