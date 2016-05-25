#!/usr/bin/env python3
#Created by xuchao on 16/5/18.
import random
# 选择菜单 g 是后边附加名称
def choice(choice=None,g='',p='y'):# choice值默认为空 g= 请选择后边要写的字 p如果传入值不打印返回上一级菜单
    List = []
    # 如果传入值
    if choice!=None:
        for i,v in enumerate(choice):
            if  type(choice) == list:#列表 打印序号,列表循环当前值
                List.append(v)
                print('{:<20}'.format(i),'{:>20}'.format(v))
            elif type(choice) == dict:#如果是字典打印序号,key,value
                List.append(v)
                print('{:<13}'.format(i),'{:^15}'.format(v),'{:>11}'.format(choice[v]))
        if p == 'y':
            print('{:<24}'.format('b'),'{:>19}'.format('返回上一级菜单'))
    Number = input('{0}:'.format(g))
    if Number.isdigit():
        return int(Number),List
    else:
        return Number,List

# 配合随机颜色
def Font_color(v=0):
    if v ==0:
        return random.randint(31, 37)
    else:
        return random.randint(40, 47)