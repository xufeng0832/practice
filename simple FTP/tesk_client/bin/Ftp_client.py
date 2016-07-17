#!/usr/bin/env python3
#Created by xuchao on 16/7/7.
import platform,os,sys
if platform.system() == 'Windows':BASE_DIR = '\\'.join(os.path.abspath('./').split('\\')[:-1])
else:BASE_DIR = '/'.join(os.path.abspath('./').split('/')[:-1])
sys.path.append(BASE_DIR)
from modules.Client_correlation import Myclient
if __name__ == '__main__':
    Myclient().run()