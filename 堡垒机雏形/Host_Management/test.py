#!/usr/bin/env python3
#Created by xuchao on 16/7/26.
#
# import paramiko
#
# # 创建SSH对象
# ssh = paramiko.SSHClient()
# # 允许连接不在know_hosts文件中的主机
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # 连接服务器
# ssh.connect(hostname='192.168.56.2', port=22, username='root', password='1')
#
# # 执行命令
# stdin, stdout, stderr = ssh.exec_command('ls')
# # 获取命令结果
# result = stdout.read()
# print(result)
# # 关闭连接
# ssh.close()

# import paramiko
#
# transport = paramiko.Transport(('192.168.56.2', 22))
# transport.connect(username='root', password='1')
#
# ssh = paramiko.SSHClient()
# ssh._transport = transport
#
# stdin, stdout, stderr = ssh.exec_command('df')
# print (stdout.read().decode())
#
# transport.close()


# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
# from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy import create_engine,Table
#
# '''
# 建立与 mysql 的连接：”数据库+api://数据库账号：密码@ip:端口/数据库s
# max_overflow:最大连接数
# echo:是否打印执行过程
# '''
# engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/test", max_overflow=5,echo=False)
#
# # 生成一个 sqlORM 基类
# Base = declarative_base()
#
# class UserProfile(Base):
#     """
#     用户基本信息存储表
#     """
#     __tablename__ = 'User_Profile'
#     ID = Column(Integer,primary_key=True,autoincrement=True)
#     UserName = Column(String(32),unique=True,nullable=False)
#     PassWord = Column(String(128),unique=True,nullable=False)
#     Permissions = Column(Integer, default=1)
#
# Base.metadata.create_all(engine)
#
# if __name__ == '__main__':
#     # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
#     name = 'xuchao'
#     passwd = '123'
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     obj = UserProfile(UserName=name, PassWord=passwd, )
#     session.add(obj)
#     session.commit()

# print(__file__,type(__file__))


import datetime

from sqlalchemy.ext.declarative import declarative_base
# 方法 例如 表, 数据类型, 主键, 外键
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index, DateTime

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Table

engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/test?charset=utf8", max_overflow=5, echo=False,
                       encoding='utf-8')

# 生成一个 sqlORM 基类
Base = declarative_base()

class OperationLog(Base):
    """
    操作日志
    """
    __tablename__ = 'operation_log'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    UserName = Column(String(32), unique=False, nullable=False)
    HostName = Column(String(32), unique=False, nullable=False)
    Command = Column(String(32), unique=False, nullable=False)
    Time = Column(DateTime())

Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
G1 = OperationLog(UserName='qq', HostName='Admin', Command='ls', Time=datetime.datetime.now())
session.add(G1)
session.commit()