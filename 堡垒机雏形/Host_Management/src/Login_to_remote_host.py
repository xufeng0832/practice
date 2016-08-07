#!/usr/bin/env python3
#Created by xuchao on 16/8/2.
import paramiko
import sys
import socket
from lib.sql_related import Sql_Add_table
from paramiko.py3compat import u

# windows does not have termios...
try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan, name, IP):
    if has_termios:
        posix_shell(chan, name, IP)
    else:
        windows_shell(chan,name, IP)


def posix_shell(chan, name, IP):
    import select

    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)
        # log = open('handle.log', 'a+', encoding='utf-8')
        flag = False
        temp_list = []
        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = u(chan.recv(1024))
                    if len(x) == 0:
                        sys.stdout.write('\r\n*** EOF\r\n')
                        break
                    if flag:
                        if x.startswith('\r\n'):
                            pass
                        else:
                            temp_list.append(x)
                        flag = False
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                if len(x) == 0:
                    break

                if x == '\t':
                    flag = True
                else:
                    temp_list.append(x)
                if x == '\r':
                    Sql_Add_table().OperationLog_add(name,IP,''.join(temp_list))
                    temp_list.clear()
                chan.send(x)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)


def windows_shell(chan,name, IP):
    # import threading
    from multiprocessing import Process
    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")
    temp_list1 = []
    flag = False
    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            if flag:
                if data.startswith('\r\n'):
                    pass
                else:
                    temp_list1.append(data)
                flag = False
            sys.stdout.write(data)
            sys.stdout.flush()

    # writer = threading.Thread(target=writeall, args=(chan,))
    writer = Process(target=writeall, args=(chan,))
    writer.start()

    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            if d == '\t':
                flag = True
            else:
                temp_list1.append(d)
            if d == '\r':
                Sql_Add_table().OperationLog_add(name, IP, ''.join(temp_list1))
                temp_list1.clear()
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass


def run(name, username, password, IP, port, ):

    tran = paramiko.Transport((IP, port,))
    tran.start_client()
    tran.auth_password(username, password)

    # 打开一个通道
    chan = tran.open_session()
    # 获取一个终端
    chan.get_pty()
    # 激活器
    chan.invoke_shell()

    interactive_shell(chan,name,IP)

    chan.close()
    tran.close()


# if __name__ == '__main__':
#     run('xuchao','1','192.168.56.2',22)