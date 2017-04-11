# Created by xuchao on 2017/3/23.
# !/usr/bin/env python
# -*- coding: utf8 -*-
import xlrd
import os, sys
from pyExcelerator import *

# sys.setdefaultencoding('utf8')

BASE_DIR = os.path.dirname(__file__)
DB_NAME = os.path.join(BASE_DIR, 'tag_path', 'db')
fname = os.listdir(DB_NAME)


def read_tags_by_path(path):
    new_table = Workbook()
    exl = new_table.add_sheet('Sheet1')
    exl.write(0, 0, "Device_ID")
    exl.write(0, 1, "Acquisition_parameters")
    line_num = 1
    for file_name in fname:
        path_name = os.path.join(DB_NAME, file_name)
        bk = xlrd.open_workbook(path_name)
        try:
            sh = bk.sheet_by_name("Sheet1")
        except:
            print "no sheet in %s named Sheet1" % fname
        nrows = sh.nrows
        for n in range(1, nrows):
            row_data = sh.row_values(n)
            Device_ID = row_data[5].split('.')[0]
            Acquisition_parameters = 'DB.Channel_1.%s.%s' % (file_name.split('.')[0], row_data[1])
            exl.write(line_num, 0, Device_ID)
            exl.write(line_num, 1, Acquisition_parameters)
            line_num += 1
    new_table.save(u'Combination point table.xls')


read_tags_by_path('db')
