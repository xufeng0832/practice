注意事项:
        1 index.py 需要有执行权限
        2 index.py所在目录有写权限
        3 解释器为python3
支持模块:
        os
        pickle
        getpass

这是一个对账号操作的小程序,内容包括 注册 登陆 修改密码 错误锁定

执行本程序后会在当前目录下自动生成两个文件:
    locking     保存锁定信息文件
    password    保存账号密码文件

1.用户注册:
    本程序拥有创建账户功能,并可检测该账户是否存在,已存在账户不可再次创建
2.登陆:
    登陆时输入账号 密码,验证正确打印欢迎信息并返回主界面,如密码连续3此输入错误则锁定该账号(该账户不可登陆)
3.修改密码:
    输入原始账号密码(同登陆效果一样,输入3次错误锁定),验证成功后输入新的密码(两次必须相同,否则无线重输)
