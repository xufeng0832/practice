#!/usr/bin/env python3
#Created by xuchao on 16/7/27.
from lib.sql_related import *



def User_Add():
    """
    添加用户
    """
    add_user = Sql_Add_table()
    username = input(' 请输入账号:')
    password = input(' 请输入密码:')
    add_user.User_add(username,password)


# User_add('xuchao','123')

# obj = Users(name="alex0", extra='sb')
# session.add(obj)
# session.add_all([
#     Users(name="alex1", extra='sb'),
#     Users(name="alex2", extra='sb'),
# ])
# session.commit()