#!/usr/bin/env python3
#Created by xuchao on 16/5/15.
import Login
import os
import time
from utility.data import Appliance
from utility.data import Clothes
from utility.data import Phone
from utility.data import Car
from utility.data import One_Menu
from utility.data import Tow_Menu_cat
from utility.data import Tow_Menu_class
from utility.data import Tow_Menu_Money
from utility.Shopping_Mall import choice
from utility.Shopping_Mall import Font_color

os.system('clear')

# 购买商品D=字典
def buy_commodity(D):
    while True:
        os.system('clear')
        print(Tow_Menu_class[erji[0]].center(50, '-'))
        sanji = choice(D, '购买商品')
        if sanji[0] == 'b':
            return
        elif type(sanji[0]) == int and sanji[0] < len(D):
            Number = choice(g='购买的商品的数量')
            if type(Number[0])==int:
                shangpin = sanji[1][sanji[0]]
                Shop_car.wirt(shangpin, D[shangpin], Number[0])
            else:
                input('\033[1;31;40m输入错误,请重新输入(按任意键继续)\033[0m')
        else:
            input('\033[1;31;40m输入错误,请重新输入(按任意键继续)\033[0m')
# 展示购物车
def Exhibition():
    Total = 0
    shop_car_list = []
    print('''{0}'''.format('购物车商品列表'.center(50, '-')))
    print('{:<10}'.format('序号'), '{:^10}'.format('商品'), '{:^10}'.format('单价'), '{:>10}'.format('数量'))
    for i, v in enumerate(Shop_car.read()):
        shop_car_list.append(v)
        print('{:<15}'.format(i), '{:<13}'.format(v), '{:<17}'.format(Shop_car.read()[v][0]),
              '{:<10}'.format(Shop_car.read()[v][1]))
        Total += Shop_car.read()[v][0] * Shop_car.read()[v][1]
    print('此次购物需花费:%s'.center(44, '-') % Total)
    return shop_car_list

ss = Login.Landing_interface()
State = False
while True:
    a = input('''
=====================================

    1 注册
    2 登陆
    3 修改密码
    4 进入商城
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
            State=True
            User_Name=user
    elif a == '3':
        if ss.Change_Ps() == True:
            print('\nPassword modification success(密码修成功)\n')
    elif a == 'q':
        print('\nEnd of program(程序结束)\n')
        break
    elif a == '4':
        if State==False:
            print('请先登录')
        else:
            Money = Login.Mone_handle(User_Name)# 初始化类时执行判断是否有过金钱记录
            Money.Mone_init()
            Shop_car = Login.shop_car(User_Name)
            History=Login.History(User_Name)
            while True:
                os.system('clear')
                print('菜单'.center(50,'-'))
                yiji = choice(One_Menu,'请选择你要进行的操作')
                # 购买商品
                if yiji[0] == 0:
                    while True:
                        os.system('clear')
                        print(One_Menu[yiji[0]].center(50, '-'))
                        erji = choice(Tow_Menu_class, '购买的商品类别')
                        if erji[0] == 0:
                            buy_commodity(Appliance)
                        elif erji[0] == 1:
                            buy_commodity(Clothes)
                        elif erji[0] == 2:
                            buy_commodity(Phone)
                        elif erji[0] == 3:
                            buy_commodity(Car)
                        elif erji[0] == 'b':
                            break
                        else:
                            input('\033[1;31;40m输入错误,请重新输入(按任意键继续)\033[0m')
                # 购物记录
                elif yiji[0] == 1:
                    os.system('clear')
                    Ht_dict = History.read()
                    if len(Ht_dict)==0:
                        input('还未在本店购物过(按任意键继续)')
                    else:
                        for i in Ht_dict:
                            Ht_Number=0
                            aa = (time.gmtime(i))
                            print(time.strftime("%Y-%m-%d %X", aa).center(49,'-'))
                            print('','|','{:<15}'.format('商品'), '{:^9}'.format('单价'), '{:>13}'.format('数量'),'|')
                            for v in Ht_dict[i]:
                                print('\033[1;{};40m'.format(Font_color()),'|','{:<15}'.format(v),'{:^9}'.format(Ht_dict[i][v][0]), '{:>15}'.format(Ht_dict[i][v][1]),'|','\033[0m')
                                jiage = Ht_dict[i][v][0]*Ht_dict[i][v][1]
                                Ht_Number+=jiage
                            print('此次购物花费:%s'.center(42,'-') % Ht_Number)
                            print()
                        input('按任意键返回购物菜单')
                # 购物车
                elif yiji[0] == 2:
                    while True:
                        os.system('clear')
                        # 打印购物车
                        if len(Shop_car.read())==0:
                            input('购物车还没东西呢赶紧去买吧(按任意键继续)')
                            break
                        else:
                            print('购物车功能'.center(50,'-'))
                            erji = choice(Tow_Menu_cat, '请输入选择')
                            # 修改商品数量
                            if erji[0]==0:
                                while True:
                                    # Total = 0
                                    os.system('clear')
                                    shop_car_list=Exhibition()
                                    print()
                                    sanji = choice(g='请输入需要修改的商品序号')
                                    if sanji[0] == 'b':
                                        break
                                    elif type(sanji[0])==int:
                                        if sanji[0] < len(shop_car_list):
                                            xiugai = choice(g='''请输入修改后的数量(0则删除该物品)''')
                                            if type(xiugai[0])==int:
                                                shop_car_primary = Shop_car.read()
                                                if xiugai[0] == 0:
                                                    Number_by=0
                                                else:
                                                    Number_by=xiugai[0]-shop_car_primary[shop_car_list[sanji[0]]][1]
                                                Shop_car.wirt(shop_car_list[sanji[0]],shop_car_primary[shop_car_list[sanji[0]]][0],Number_by)
                                            else:input('\033[1;31;40m输入错误,请重新输入(按任意键继续)\033[0m')
                                            if len(Shop_car.read()) == 0:
                                                print('购物车空了')
                                                break
                                        else:
                                            input('\033[1;31;40m输入错误,请重新输入(按任意键继续)\033[0m')
                                    else:input('\033[1;31;40m输入错误,请重新输入(按任意键继续)\033[0m')
                            elif erji[0] == 1:#结账
                                os.system('clear')
                                if Money.See() >= Shop_car.jiezhang():#自己的钱是否大于购物车的金钱
                                    balance=Money.See()-Shop_car.jiezhang()
                                    Money.Mone_reduce(Shop_car.jiezhang())
                                    history=Shop_car.read()
                                    Now_time = time.time() + 28800
                                    History.wirt(Now_time,**history)
                                    Shop_car.empty_shuo_car()
                                    print('购买成功')
                                    input('您的余额:{0}  (按任意键继续)'.format(balance))
                                    break
                                else:
                                    print('您的余额:{0}-------购物总价格{1}'.format(Money.See(),Shop_car.jiezhang()))
                                    input('您的余额不足请及时充值(按任意键继续)')
                            elif erji[0] ==2:
                                os.system('clear')
                                Exhibition()
                                input('(按任意键继续)')
                            elif erji[0] == 'b':
                                break
                            else:
                                input('\033[1;31;40m输入错误,请重新输入(按任意键继续)\033[0m')
                elif yiji[0] == 3:
                    while True:
                        os.system('clear')
                        print('请选择需要做的:'.center(50, '-'))
                        erji = choice(Tow_Menu_Money, '请输入选择')
                        if erji[0] == 0:
                            os.system('clear')
                            input('您的余额:{:^9} (按任意键继续)'.format(Money.See()))
                        elif erji[0] == 1:
                            os.system('clear')
                            sanji = choice(g='请输入您要存入的金额')
                            if type(sanji[0]) == int:
                                Money.Mone_add(sanji[0])
                                balance = Money.See()
                                input('存储成功您的余额为:{0}'.format(balance))
                            else:
                                input('请输入正确的金额!(按任意键继续)')
                        elif erji[0] =='b':
                            break
                        else:
                            os.system('clear')
                            input('\033[1;31;40m输入错误,请重新输入(按任意键继续)\033[0m')
                elif yiji[0] == 'b':
                    os.system('clear')
                    break
                else:
                    input('\033[1;31;40m输入错误,请重新输入(按任意键继续)\033[0m')
    else:
        print('\n请输入正确的选项\n')