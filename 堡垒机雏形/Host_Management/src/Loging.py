#!/usr/bin/env python3
#Created by xuchao on 16/7/29.
from src.Admin import *
from src.Employess import *

def Determine():
    select = Sql_query()
    for i in range(3):
        username = input('账号:')
        password = input('密码:')
        sql_user = select.select_User(username)
        if sql_user:
            if sql_user.PassWord == password:return sql_user
            else:print('密码错误')
        else:
            print('该账号不存在')

# 是否登陆成功
def login():
    user = Determine()
    if user:
        Determine_the_interface(user)

# 判断用户权限
def Determine_the_interface(user):
    if user.Permission == 1:
        administrator_interface(user)
    if user.Permission == 2:
        Employees_interface(user)



# from db.db_init_ import sql_session
# session=sql_session()






# login()