#!/usr/bin/env python3
#Created by xuchao on 16/7/29.
import platform,os,sys
if platform.system() == 'Windows':BASE_DIR = '\\'.join(os.path.abspath('./').split('\\')[:-1])
else:BASE_DIR = '/'.join(os.path.abspath('./').split('/')[:-1])
sys.path.append(BASE_DIR)
from db.db_init_ import *
import subprocess


# subprocess.Popen('echo %s>> /etc/profile')
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


session=sql_session()

User_init = UserProfile(ID=1, UserName='root', PassWord='123', Permission=1)
P1= Authority(ID=1, Name='Administrator')#管理员
P2 = Authority(ID=2, Name='Employees')#员工
G1 = ServerGroup(ID=1, Name='Admin')
session.add_all([User_init, P1, P2, G1])

ret = session.query(UserProfile).filter_by(UserName='root').first()
ret1 = session.query(Authority).filter_by(Name='Administrator').first()
U_P1 = UserToAuthority(Authority_Id=ret1.ID, User_Id=ret.ID)
U_G1 = UserToGroup(User_Id=1, Group_Id=1)

session.add_all([U_P1,U_G1])
session.commit()
# session.add(obj)
# session.add_all([