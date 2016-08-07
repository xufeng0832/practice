#!/usr/bin/env python3
#Created by xuchao on 16/7/31.

# 创建基类时需要的
from sqlalchemy.ext.declarative import declarative_base
# 方法 例如 表, 数据类型, 主键, 外键
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index, DateTime

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Table

'''
建立与 mysql 的连接：”数据库+api://数据库账号：密码@ip:端口/数据库s
max_overflow:最大连接数
echo:是否打印执行过程
'''
engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/s13?charset=utf8", max_overflow=5, echo=False,
                       encoding='utf-8')

# 生成一个 sqlORM 基类
Base = declarative_base()


class HostToGroup(Base):
    """
    关联 Host 和 Group
    """
    __tablename__ = 'Host_To_Group'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Server_Id = Column(Integer, ForeignKey('Server_Host.ID'))
    Group_Id = Column(Integer, ForeignKey('Server_Group.ID'))
    __table_args__ =(UniqueConstraint('Server_Id','Group_Id',name='uix_sid_gid'))# 联合唯一
    # group = relationship('ServerGroup', backref='s1g')
    # host = relationship('ServerHost', backref='s2g')


class UserToGroup(Base):
    """
    关联 user 和 Group
    """
    __tablename__ = 'User_To_Group'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    User_Id = Column(Integer, ForeignKey('User_Profile.ID'))
    Group_Id = Column(Integer, ForeignKey('Server_Group.ID'))
    __table_args__ =(UniqueConstraint('User_Id','Group_Id',name='uix_uid_gid'))
    # group = relationship('ServerGroup', backref='s3g')
    # user = relationship('UserProfile', backref='s4g')


class UserToAuthority(Base):
    """
    关联 用户 和 权限
    """
    __tablename__ = 'User_To_Authority'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Authority_Id = Column(Integer, ForeignKey('User_Authority.ID'))
    User_Id = Column(Integer, ForeignKey('User_Profile.ID'))
    __table_args__ =(UniqueConstraint('Authority_Id','User_Id',name='uix_aid_uid'))
    # authority = relationship('Authority', backref='s5g')
    # user = relationship('UserProfile', backref='s6g')


class UserProfile(Base):
    """
    用户基本信息存储表
    """
    __tablename__ = 'User_Profile'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    UserName = Column(String(32), unique=True, nullable=False)
    PassWord = Column(String(128), unique=False, nullable=False)
    Permission = Column(Integer, default=2)
    host_permission = relationship('Authority',secondary=UserToAuthority.__table__,backref='user')
    group = relationship('ServerGroup',secondary=UserToGroup.__table__,backref='user')


class Authority(Base):
    """
    权限分级信息表
    """
    __tablename__ = 'User_Authority'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(64), nullable=False, unique=True)


class ServerGroup(Base):
    """
    服务器主机组信息表
    relationship:关联类
    #     做一个类映射成原生的表结构
    #     Column:字段属性
    #     Integer:数据类型(整数)
    #     String:数据类型(字符串)
    #     primary_key: 主键
    #     unique:唯一约束(值不可重复)
    #     autoincrement:是否自增
    """
    __tablename__ = 'Server_Group'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(64), nullable=False, unique=True)
    host = relationship('ServerHost', secondary=HostToGroup.__table__, backref='group')


class ServerHost(Base):
    """
    服务器主机信息表
    nullable:是否可以为空
    """
    __tablename__ = 'Server_Host'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Host_Name = Column(String(64), unique=True, nullable=False)
    IP_addr = Column(String(128), unique=True, nullable=False)
    Port = Column(Integer, default=22)
    UserName = Column(String(32), unique=False, nullable=False)
    PassWord = Column(String(128), unique=False, nullable=False)


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



# 删除所有表结构,不存在则忽略
# Base.metadata.drop_all(engine)
# # 创建所有表结构,存在则忽略
# Base.metadata.create_all(engine)



# if __name__ == '__main__':
#     # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
#     name = 'xuchao'
#     passwd = '123'
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     obj = UserProfile(UserName=name, PassWord=passwd)
#     session.add(obj)
#     session.commit()

def sql_session():
    Session = sessionmaker(bind=engine)
    return Session()

# session=sql_session()

# User_init = UserProfile(ID=1, UserName='root', PassWord='123', Permission=1)
# P1= Authority(ID=1, Name='Administrator')#管理员
# P2 = Authority(ID=2, Name='Employees')#员工
# session.add_all([User_init, P1, P2,])
#
# ret = session.query(UserProfile).filter_by(UserName='root').first()
# ret1 = session.query(Authority).filter_by(Name='Administrator').first()
# U_P1 = UserToAuthority(Authority_Id=ret1.ID, User_Id=ret.ID)
# session.add(U_P1)
# session.commit()

'''查询'''

# ret001 = session.query(UserProfile).filter(UserProfile.UserName=='root').first()
# for i in ret001.s6g:
#     print(i.authority.Name)
#
# print(ret001.host[0].Name)

# ret001 = session.query(UserProfile).filter(UerProfile.UserName=='root').first()
# # print(ret001.host.ID)
# for i in ret001.host:
#     print(i.ID)