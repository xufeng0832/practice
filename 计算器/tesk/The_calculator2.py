#!/usr/bin/env python3
#Created by xuchao on 16/6/13.

import re
# 计算乘除
def Multiplication_and_division(arg):
    while True:
        # 函数不可直接改变变量,可以给列表中的元素重新赋值
        source =arg[0]
        # 任意数字(\d+1到多个),任意字符点(\.*零到多个),任意数字(\d*零到多个) 例如23.5 3
        # *或/([\*\/]+ 1个以上),+或-([\+\-]? 一个或0用于判断正负数)  例如2*-2  2*4
        # 任意数字(\d+1到多个),任意字符点(\.*零到多个),任意数字(\d*零到多个) 例如23.5 3
        result= re.search('\d+\.*\d*[\*\/]+[\+\-]?\d+\.*\d*', source)
        if not result:
            return
        # 拿到第一个匹配到的值
        content=re.search('\d+\.*\d*[\*\/]+[\+\-]?\d+\.*\d*', source).group()
        # 以乘号分隔
        if len(content.split('*'))>1:
            n1, n2 = content.split('*')
            value = float(n1) * float(n2)
        else:
            n1, n2 = content.split('/')
            value = float(n1) / float(n2)
        before, after = re.split('\d+\.*\d*[\*\/]+[\+\-]?\d+\.*\d*', source, 1)
        new_str = "%s%s%s" % (before, value, after)
        arg[0] = new_str
# 计算加减
def Add_and_subtract(arg):
    while True:
        # 替换加法加负数的显示方式
        if '+-' in arg[0] or '++' in arg[0] or '-+' in arg[0] or '--' in arg[0]:
            arg[0] = arg[0].replace('+-', '-')
            arg[0] = arg[0].replace('++', '+')
            arg[0] = arg[0].replace('-+', '-')
            arg[0] = arg[0].replace('--', '+')
        # 如果是开头是负数 那么把所有数变变反,之后截到开头的+
        if arg[0].startswith('-'):
            arg[1] = 1
            arg[0] = arg[0].replace('-','><')
            arg[0] = arg[0].replace('+','-')
            arg[0] = arg[0].replace('><','+')
            arg[0] = arg[0][1:]
        source = arg[0]
        # 任意数字(\d+1到多个),任意字符点(\.*零到多个),任意数字(\d*零到多个) 例如23.5 3
        # 加或减([\+\-]{1})
        # 任意数字(\d+1到多个),任意字符点(\.*零到多个),任意数字(\d*零到多个) 例如23.5 3
        resule = re.search('\d+\.*\d*[\+\-]{1}\d+\.*\d*',source)
        if not resule:
            return
        # 拿到第一个匹配到的值
        content = re.search('\d+\.*\d*[\+\-]{1}\d+\.*\d*', source).group()
        # 以+号分隔
        if len(content.split('+')) > 1:
            n1, n2 = content.split('+')
            value = float(n1) + float(n2)
        else:
            n1, n2 = content.split('-')
            value = float(n1) - float(n2)

        before, after = re.split('\d+\.*\d*[\+\-]{1}\d+\.*\d*', source, 1)
        # 新值拼接
        new_str = "%s%s%s" % (before, value, after)
        arg[0] = new_str

# 计算加减乘除
def compute(arg):
    # [表达式,正负]    正 0  负1
    inp = [arg,0]
    # 处理乘除
    Multiplication_and_division(inp)
    # 处理加减
    Add_and_subtract(inp)
    # 判断是否是负数
    if inp[1]:
        result = float(inp[0])
        result = result * -1
        inp[1]=0
    else:
        result = float(inp[0])
    return result

# 处理括号
def brackets(arg):
    # 包含(的   \(
    # 加或减或乘或除零到多次(第一次可以处理正负号)   \(([\+\-\*\/]*  , -2 +3(在括号里)
    # 一个以上的数字,点零到多次,零到多次的数字   *\d+\.*\d*     2  2.3333
    # 匹配的内容 出现两次以上 {2,}     -23.2*+23    32/12.3
    # 包含)的   \)           和前面的(组合)         (获取 第一个 只含有 数字/小数 和 操作符 的括号)
    while True:
        if not re.search('\(([\+\-\*\/]*\d+\.*\d*){2,}\)', arg):
            final_result = compute(arg)
            return final_result
        # 截取第一个匹配到的字符串
        content = re.search('\(([\+\-\*\/]*\d+\.*\d*){2,}\)', arg).group()
        # 分割为三段 匹配之前  匹配中   匹配后
        # 匹配中 因为带有()组元素 所以只得到组之外的元素
        # 类似re.search('\(([\+\-\*\/]*\d+\.*\d*){2,}\)', arg).groups()的到的结果
        # nothing 这个值我们用不到,在之前已经用group截取到了
        before, nothing, after = re.split('\(([\+\-\*\/]*\d+\.*\d*){2,}\)', arg, 1)
        # 打印之前的表达式
        print('之前的表达式：', arg)
        # 剥除括号
        content = content[1:len(content) - 1]
        # 计算
        ret = compute(content)
        # 打印 计算过程
        print('计算 %s=%s' % (content, ret))
        # 将执行结果拼接
        arg = "%s%s%s" %(before, ret, after)
        print ('本次计算结果 ：',arg)
        print ("="*10,'上一次计算结束',"="*10)
        # 重复操作直到没有括号

def interactive():
    while True:
        inpp = input('请输入你想计算的表达式:')
        # 去除表达式中多余的空格
        inpp = re.sub('\s*', '', inpp)
        # 表达式保存在列表中
        result = brackets(inpp)
        print(result)

if __name__ == '__main__':
    interactive()

# 1 - 2 * ( (60-30 +(-40.0/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )