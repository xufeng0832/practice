#!/usr/bin/env python3
#Created by xuchao on 16/8/3.
import platform,os,sys
if platform.system() == 'Windows':BASE_DIR = '\\'.join(os.path.abspath(__file__).split('\\')[:-2])
else:BASE_DIR = '/'.join(os.path.abspath(__file__).split('/')[:-2])
print(BASE_DIR)
sys.path.append(BASE_DIR)
from src.Loging import *
if __name__ == '__main__':
    login()