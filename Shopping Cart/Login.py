#!/usr/bin/env python3
#Created by xuchao on 16/5/15.
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

# 金钱处理
class Mone_handle(object):
    def __init__(self,name):
        self.__f = File_handle('./Money')
        self.__name = name
    # 判断是否没有输入金额
    def Mone_init(self):
        Mone = self.__f.read()
        if self.__name not in Mone:
            Mone[self.__name]=int(input('请输入你的资产:'))
            self.__f.wirt(**Mone)
        return Mone[self.__name]
    def See(self):
        return self.__f.read()[self.__name]
    # 存钱
    def Mone_add(self,qian):
        Mone = self.__f.read()
        Mone[self.__name]+=qian
        self.__f.wirt(**Mone)
    #     减钱
    def Mone_reduce(self,qian):
        Mone = self.__f.read()
        Mone[self.__name]-=qian
        self.__f.wirt(**Mone)
# 登陆
def Login():
    user = Landing_interface.Login()
    if user != False:
        print('\nWelcome {0} landing(欢迎 {0} 登陆)\n'.format(user))
        return user

class shop_car(object):
    def __init__(self,name):
        # 初始化文件
        self.__f = File_handle('./Shop_Car')
        self.__name = name
        shop_car = self.__f.read()
        # 初始化用户在字典里的信息
        if self.__name not in shop_car:
            # 用户{商品名称:{价格:数量}
            shop_car[self.__name]={}
            self.__f.wirt(**shop_car)
    def read(self):
        shop_car = self.__f.read()
        return shop_car[self.__name]# '商品':[价格:数量]
    # 新增购物车记录 接收{商品:[价格,数量]
    def wirt(self,Product,Price,Number):
        big_ditc = self.__f.read()
        if  Product in big_ditc[self.__name]:
            if Number == 0:
                del big_ditc[self.__name][Product]
            else:
                jiageshul = big_ditc[self.__name][Product]
                jiageshul[1]+=Number
                big_ditc[self.__name][Product]=jiageshul
        else:
            big_ditc[self.__name][Product]=[Price,Number]

        self.__f.wirt(**big_ditc)
    def jiezhang(self):
        mani = 0
        for i in self.read():
            mani+=self.read()[i][0]*self.read()[i][1]
        return mani
    def empty_shuo_car(self):
        big_ditc = self.__f.read()
        big_ditc[self.__name]={}
        self.__f.wirt(**big_ditc)

class History(object):
    def __init__(self, name):
        # 初始化文件
        self.__f = File_handle('./History_purchase')
        self.__name = name
        shop_car = self.__f.read()
        # 初始化用户在字典里的信息
        if self.__name not in shop_car:
            # 用户{时间:{商品:[单价,数量]}
            shop_car[self.__name] = {}
            self.__f.wirt(**shop_car)

    def read(self):
        shop_car = self.__f.read()
        return shop_car[self.__name]  # 时间:[单价:数量]
    # 时间{商品:{单价:数量}}
    def wirt(self, time,**dict):
        big_ditc = self.__f.read()
        big_ditc[self.__name][time]=dict
        self.__f.wirt(**big_ditc)