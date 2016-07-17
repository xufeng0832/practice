#!/usr/bin/env python3
#Created by xuchao on 16/7/7.
import platform,os,sys,socketserver
if platform.system() == 'Windows':BASE_DIR = '\\'.join(os.path.abspath('./').split('\\')[:-1])
else:BASE_DIR = '/'.join(os.path.abspath('./').split('/')[:-1])
sys.path.append(BASE_DIR)
from modules.Server_correlation import MyServer
from conf.Ftpconf import SERVER
if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer((SERVER.get('IP'),SERVER.get('PORT')),MyServer)
    server.serve_forever()