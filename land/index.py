#!/usr/bin/env python3
#Created by xuchao on 16/5/10.
import getpass
import pickle
import os
# 文件处理
class File_handle(object):
    def __init__(self,File):#判断文件是否存在
        self.__file = File
        if os.path.exists(self.__file) == False:
            a={}
            self.wirt(**a)

    def read(self):# 读取数据
        with open(self.__file,'rb') as f:
            locking_r = pickle.load(f)
            return locking_r

    def wirt(self,**args):# 保存数据
        with open(self.__file,'wb') as f:
            pickle.dump(args,f)
            return 'success'

class Landing_interface(object):
    def __init__(self):
        self.__locking = File_handle('./locking')# 锁定表
        self.__password = File_handle('./password')# 密码表

    def __Input_info(self):# 接收数据
        User_name = input('\nPlease enter your account(请输入你的账号):')
        Pass_word = getpass.getpass('Please enter a password(请输入你的密码):')
        os.system('clear')
        return [User_name,Pass_word]#账号密码

    def Login(self):#登陆验证
        while True:
            data_info = self.__Input_info()#用户名 密码
            a = self.__locking.read()
            b = self.__password.read()
            if (len(data_info[0])) == 0 and len(data_info[1]) == 0:
                print('Account or password can not be empty(账号或密码不能为空)')
                continue
            if data_info[0] not in a:
                a[data_info[0]]=0# 字典a
            if a[data_info[0]]>2:#判断是否锁定  用户名在字典中,次数大于2
                print('\nYour account has been locked, please contact the administrator.(你的账号已被锁定,请联系你的管理员)\n')
                return False

            elif data_info[0] in b and b[data_info[0]] == data_info[1]:#输入正确返回用户名
                a[data_info[0]] = 0
                self.__locking.wirt(**a)
                return data_info[0]
            else:
                a[data_info[0]]+=1#字典里次数+1
                self.__locking.wirt(**a)
                print('\nAccount or password error, please re-enter(账号或密码错误,请重新输入)\n')

    def register(self):# 注册
        data_info = self.__Input_info()
        a = self.__password.read()
        b = self.__locking.read()
        if data_info[0] not in a:
            a[data_info[0]]=data_info[1]
            b[data_info[0]]=0#初始化锁定次数
            self.__password.wirt(**a)
            self.__locking.wirt(**b)#解决刚注册就被已经被锁定的bug
            return True
        else:
            print('\nThe user already exists(这个用户名已存在)\n')
            return False

    def Change_Ps(self):
        a = self.__password.read()
        user_data = self.Login()
        if user_data is not False:
            while True:
                pwd =getpass.getpass('Please enter a new password(请输入一个新密码):')
                if pwd == getpass.getpass('Please input again(请再次输入):'):
                    a[user_data] = pwd
                    self.__password.wirt(**a)
                    return True
                else:
                    os.system('clear')
                    print('\nInput error, please re-enter输入错误,请重新输入\n')

ss = Landing_interface()
while True:
    a = input('''
=====================================

    1 注册
    2 登陆
    3 修改密码
    q 退出

=====================================

    请输入:''')
    os.system('clear')
    if a == '1':
        if ss.register() == True:
            print('\nAccount registration success(账号注册成功)\n')
    elif a == '2':
        user = ss.Login()
        if user != False:
            print('\nWelcome {0} landing(欢迎 {0} 登陆)\n'.format(user))
    elif a == '3':
        if ss.Change_Ps() == True:
            print('\nPassword modification success(密码修成功)\n')
    elif a == 'q':
        print('\nEnd of program(程序结束)\n')
        break
    else:
        print('\n请输入正确的选项\n')
