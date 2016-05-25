#!/usr/bin/env python3
#Created by xuchao on 16/5/22.
from task.conf.conf import HAPROXY
from prettytable import PrettyTable
import os
import time


HAPROXY_OLD = HAPROXY+'_old'
HAPROXY_NEW = HAPROXY+'_new'
TIME = time.strftime("%F_%T")
FUNCTION=('查看节点','添加节点','添加ha记录','删除节点','删除ha记录','程序退出')



def Show_index():
    x = PrettyTable(["Number", "function"])
    x.align["Number"] = "i"
    x.padding_width = 2
    for i,v in enumerate(FUNCTION):
        if i+1==len(FUNCTION):
            i-=i+1
        x.add_row([i+1,v])
    print(x)


# 选择
def choice(arg):
    """
    判断用户输入的是否是正数,
    :param arg: 接收一个参数传入input函数
    :return: 如果是输入的是正数返回int,否则返回字符串
    """
    while True:
        os.system('clear')
        Num = input(arg)
        if Num.isdigit():
            return int(Num)
        else:print('请输入正确的选项:')


# 展示所有节点并返回一个需要查看节点的序号
def Node_subscript(arg):
    """
    打印所有节点信息并返回用户输入
    :return: 返回用户输入
    """
    a = Acquisition_node()
    x = PrettyTable(["Number", "Node"])
    x.align["Number"] = "i"
    x.padding_width = 2
    for i,v in enumerate(a):
        x.add_row([i+1,v])
    print(x)
    while True:
        Num =choice(arg)
        if Num <= len(a) and Num>0:
            return Num
        else:
            print('请输入正确的选项')

# 展示ha记录
def ha_record(arg):
    """
    接收所有的ha记录格式化打印
    :param arg: 接收一个可被迭代ha记录
    :return:
    """
    x = PrettyTable(["Number", "Ha record"])
    x.align["Number"] = "i"
    x.padding_width = 2
    for i,v in enumerate(arg):
        x.add_row([i+1,v.strip()])
    print(x)

# 返回一个元组(节点,[节点ha],序号)
def show_record(arg):
    """
    返回一个元组包含 (节点,[节点ha])
    :param arg: 给input传入一个值
    :return:(节点,[节点ha],序号)
    """
    zong=Acquisition_node()
    da = Node_subscript(arg)
    n1 = zong[da-1]
    n2 = Access_record(da)
    return n1,n2,da


# 获取文件所有节点
def Acquisition_node():
    """
    获取Ha配置文件的所有节点
    :return: 返回配置文件下所有的节点名称
    """
    a = []
    with open(HAPROXY_OLD, 'r') as f:
        for i in f.readlines():
            if 'backend' == i[:7]:
                a.append(i.replace('\n',''))
    return a


# 获取节点下的ha记录
def Access_record(num):
    """
    返回接收节点的ha记录
    :param num: 接收一个节点信息
    :return: 返回该节点下的所有记录
    """
    a = []
    sign = False
    with open(HAPROXY_OLD, 'r') as f:
        count =1
        for i in f.readlines():
            if 'backend' == i[:7]:
                if count == num:
                    sign = True
                    count+=1
                    continue
                else:count+=1
            if sign == True:
                if i[:8].isprintable():
                    a.append(i.replace('\n',''))
                else:
                    sign = False
    return a

def input_node():
    """
    返回填写的节点
    :return: 返回节点信息
    """
    return {'backend':input('backend:')}


def parameter():
    """
    返回填写的ha记录
    :return: 返回ha记录
    """
    a=input('server:')
    b=input('weight:')
    c=input('maxconn:')
    return {'server':a,'weight':b,'maxconn':c}

# 选择判断y n
def judge(arg):
    """
    判断输入 是y 还是n  默认为y
    :param arg: 传入input函数中
    :return:
    """
    while True:
        yn=input(arg)
        if  yn == 'y':
            return True
        elif yn == 'n' or yn == '':
            return False


# 添加节点
def Add_node():
    """
    添加一个节点并添加ha记录,如果该节点存在提示是否继续
    :return:
    """
    node = Acquisition_node()
    sign = True
    with open(HAPROXY_OLD, 'r') as f1 , open(HAPROXY_NEW, 'w') as f2:
        for i in f1.readlines():
            if 'backend' in i.split(' ') and sign == True:
                server = input_node()
                server_info = parameter()
                ser = ['backend',server['backend']]
                ser_in = ['       ','server',server_info['server'],server_info['server'],'weight',server_info['weight'],'maxconn',server_info['maxconn']]
                if ' '.join(ser) in node:
                    yn = judge('该节点已存在是否重复添加(n)     y/n:')
                    if yn == True:
                        pass
                    else:
                        f2.write(i)
                        sign = False
                        continue
                f2.write(' '.join(ser))
                f2.write('\n')
                f2.write(' '.join(ser_in))
                f2.write('\n')
                f2.write('\n')


                sign = False
            f2.write(i)

# 添加ha记录
def Add_record(num,ha):
    """
    添加节点下的ha记录
    :param node: 需要添加ha记录的节点编号
    :param ha: 该节点下所有的ha记录
    :return:
    """
    with open(HAPROXY_OLD, 'r') as f1 , open(HAPROXY_NEW, 'w') as f2:
        count = 1
        for i in f1.readlines():
            f2.write(i)
            if 'backend' == i[:7]:#是backend
                if count == num:
                    server_info = parameter()
                    ser_in = ['       ','server',server_info['server'],server_info['server'],'weight',server_info['weight'],'maxconn',server_info['maxconn']]
                    if ser_in[2] in ''.join(ha).split(' '):
                        yn = judge('该节点已存在是否重复添加(y)     y/n:')
                        if yn == True:
                            pass
                        else:
                            f2.write(i)
                            continue
                    f2.write(' '.join(ser_in))
                    f2.write('\n')
                else:count+=1

# 删除节点
def del_node(Num):
    """
    记录所有节点并根据 Num 记录值删除 该节点和该节点的ha记录
    :param Num: 接收一个想要删除的数字
    :return:
    """
    node = Acquisition_node()
    sign=''
    with open(HAPROXY_OLD, 'r') as f1, open(HAPROXY_NEW, 'w') as f2:
        count = 1
        for i in f1.readlines():
            if 'backend' == i[:7]:
                if count ==Num:
                    sign=True
                    count+=1
                else:
                    count+=1
                    sign=''
            if sign==True:
                if node[Num-1] == i.strip():
                    sign=False
                else:
                    sign=True
            if sign == False:
                continue
            f2.write(i)


# 删除节点ha记录
def del_record():
    """
    show_record记录需要改变ha的节点,
    Access_record获取所有节点
    choice 记录需要删除的ha记录
    删除
    :return:
    """
    Show = show_record('选择想要删除ha记录的节点:')
    node = Access_record(Show[2])
    sign = ''
    if len(Show[1]) < 1:
        print('该节点下无ha记录')
        return
    for i,v in enumerate(Show[1]):
        print(i+1,v)
    while True:
        num = choice('请输入想要删除的ha记录')
        if num <= len(node) and num >0:
            break
        else:print('输入错误请重新输入')
    with open(HAPROXY_OLD, 'r') as f1,open(HAPROXY_NEW, 'w') as f2:
        count=1
        for i in f1.readlines():
            if 'backend' == i[:7]:
                if count == Show[2]:
                    sign = True
                    count+=1
                else:count+=1
            if sign == True:
                if i.strip('\n') == Show[1][num-1]:
                    sign=False
                    continue
            f2.write(i)
# 配置文件处理
class File_handle(object):
    def __init__(self):
        pass
    def Copy(self):
        # 复制Ha配置文件生成一个临时的配置文件
        os.system('cp %s %s'%(HAPROXY,HAPROXY_OLD))
    def Delete(self):
        # 删除ha的临时配置文件
        os.system('rm -rf %s'%HAPROXY_OLD)
    def Update(self):
        # 更新Ha的临时配置文件
        if os.path.exists(HAPROXY_NEW):
            self.Delete()
            os.system('mv %s %s'%(HAPROXY_NEW,HAPROXY_OLD))
        else:pass
    def application(self):
        # 应用配置
        os.system('mv %s %s'%(HAPROXY,HAPROXY+'.bak_%s'%(TIME)))
        os.system('mv %s %s'%(HAPROXY_OLD,HAPROXY))
