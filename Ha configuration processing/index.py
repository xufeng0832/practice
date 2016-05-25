#!/usr/bin/env python3
#Created by xuchao on 16/5/22.
from utility.File_modification import Acquisition_node
from utility.File_modification import Node_subscript
from utility.File_modification import show_record
from utility.File_modification import Access_record
from utility.File_modification import choice
from utility.File_modification import Add_node
from utility.File_modification import Add_record
from utility.File_modification import del_node
from utility.File_modification import del_record
from utility.File_modification import File_handle
from utility.File_modification import ha_record
from utility.File_modification import Show_index

DATA_CHANGES = False
def main():
    File=File_handle()
    File.Copy()
    while True:
        Show_index()
        Num = choice('''请输入:''')
        # 查看节点的参数
        if  Num == 1:
            Show = show_record('选择想要查看的节点:')
            print(Show[0])
            ha_record(Show[1])
            # for i in Show[1]:
            #     print(i)
        elif Num == 2 :
            Add_node()

        elif Num == 3 :
            node_num = Node_subscript('你想添加哪个节点的ha记录:')
            ha = Access_record(node_num)
            Add_record(node_num, ha)

        elif Num == 4:
            Zong = Acquisition_node()
            da = Node_subscript('选择想要删除的节点:')
            if da <= len(Zong):
                del_node(da)

        elif Num == 5:
            del_record()

        elif Num == 0:
            while True:
                Ext = input('配置保存配置文件(y)      y/n:')
                if Ext == 'y' or Ext == ' ':
                    global DATA_CHANGES
                    DATA_CHANGES = True
                    break
                elif Ext =='n':
                    File.Delete()
                    return
        else:print('请输入正确的选项')
        File.Update()
        if DATA_CHANGES == True:
            File.application()
            return
        else:pass


if __name__ == '__main__':
    main()