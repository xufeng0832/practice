#!/usr/bin/env python
# coding=utf-8
# Created by xuchao on 2017/4/6.
import sys, time, os, signal
import sqlite3
from prettytable import PrettyTable


class SvnToOnline:
    def __init__(self, name):
        self.name = name
        self.update_list = []
        self.time_path = time.strftime('%Y-%m-%d')
        self.now_time = time.strftime('%H:%M:%S')
        self.cursor = DBoperations()
        self.back_path = self.cursor.get_configuration_file()[2].encode("utf-8")
        self.online_path = self.cursor.get_configuration_file()[0].encode("utf-8")
        self.svn_path = self.cursor.get_configuration_file()[1].encode("utf-8")
        self.Check_The_Environment()

    def create_file_not_exist(self, path):
        """If the file not exist then create"""
        if not os.path.exists(path):
            os.mkdir(path, 0755)
        return path

    def Check_The_Environment(self):  # Check the path exists
        try:
            self.create_file_not_exist(self.back_path + self.time_path)
            self.now_bak = self.create_file_not_exist(self.back_path + self.time_path + '/' + self.now_time)
        except:
            print('permission deny')

    def Get_Update_File(self):  # get to update files
        with open('%s' % self.name_path, 'r') as fname:
            for i in fname.readlines():
                i = i.strip()
                if i == '...':
                    break
                self.update_list.append(i)
        # print(self.online_path)
        os.system('svn up %s' % self.svn_path)
        # subprocess.check_output('svn up %s' % self.svn_path)

    def File_Operations(self, note=None):  # Update files and records
        save_list = []
        for i in self.update_list:
            os.system('cp {0}{1} {2}'.format(self.online_path, i, self.now_bak))
            os.system('cp {1}{0} {2}{0}'.format(i, self.svn_path, self.online_path))
            save_list.append((self.now_time, note, self.online_path + i, os.path.join(self.now_bak, i.split('/')[-1]),
                              self.name))
        self.cursor.save_history(save_list)


class DBoperations:
    def __init__(self):
        if not os.path.exists('./db.sqlite3'):
            self.cx = sqlite3.connect("./db.sqlite3")
            self.cx.execute('CREATE TABLE "config" ('
                            '"id" INTEGER NOT NULL PRIMARY KEY,'
                            '"online_path" TEXT NOT NULL,'
                            '"svn_path" TEXT NOT NULL,'
                            '"backup_path" TEXT NOT NULL)')
            self.cx.execute('CREATE TABLE "history" ('
                            '"id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
                            '"name" TEXT NOT NULL,'
                            '"time" TEXT NOT NULL,'
                            '"back_file" TEXT NOT NULL,'
                            '"online_file" TEXT NOT NULL,'
                            '"note" TEXT)')

            self.cx.execute('INSERT INTO "config" VALUES (1, "/test/Logan/", "/test/PHP/", "/backup/")')
            self.cx.commit()
        else:
            self.cx = sqlite3.connect("./db.sqlite3")

    def get_configuration_file(self):
        # sd = self.cx.execute("SELECT * FROM config")
        sd = self.cx.execute("SELECT config.online_path, config.svn_path, config.backup_path FROM config WHERE id=1")
        return sd.fetchone()

    def get_historical(self, num):
        sd = self.cx.execute("SELECT * FROM history")
        return sd.fetchmany(num)

    def save_history(self, data):
        for li in data:
            self.cx.execute(
                    'INSERT INTO "history" ( "time", "note", "online_file", "back_file", "name") VALUES (?,?,?,?,?)',
                    li)
        self.cx.commit()

    def save_config(self, data):
        self.cx.execute("UPDATE config SET 'online_path'=(?),'svn_path'=(?),'backup_path'=(?) WHERE id = 1", data)
        self.cx.commit()


class View:
    def __init__(self):
        self.cursor = DBoperations()
        name = raw_input('请输入需要更新文件路径文件>>> ')
        name_path = self.check_file(name)
        if name_path:
            self.file_cursor = SvnToOnline(name)
            self.file_cursor.name_path = name_path
        else:
            exit('输入错误程序退出!')

    def check_file(self, name):
        if not name:
            return False
        name_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
        if os.path.exists(name_path):
            return name_path

    def start(self):
        while True:
            choose = raw_input("""
            1       配置文件路径
            2       更新
            3       查看最近更新记录
            0       退出
请输入>>> """)
            if choose == '1':
                self.modify_config()
            elif choose == '2':
                self.update()
            elif choose == '0':
                exit('程序结束!')
            elif choose == '3':
                self.history_record()
            else:
                print('输入错误')

    def modify_config(self):
        print("""
输出格式>>> /xx/xxx/
        """)
        online_path = raw_input('线上路径:')
        svn_path = raw_input('SVN路径:')
        backup_path = raw_input('备份路径:')
        data = (online_path, svn_path, backup_path)
        self.validity_check(data)
        if self.flag:
            self.cursor.save_config(data)
        else:
            print('格式错误')

    def validity_check(self, data):
        self.flag = True
        for i in data:
            if not i.startswith('/') or not i.endswith('/'):
                self.flag = False

    def update(self):
        note = raw_input('注释:')
        self.file_cursor.Get_Update_File()
        self.file_cursor.File_Operations(note=note)

    def history_record(self):
        choonse = raw_input('查询最近多少条数据>>> ')
        if choonse.isdigit():
            history_list = self.cursor.get_historical(int(choonse))
            history_list.reverse()
        else:
            exit('输入错误!')
        x = PrettyTable(["版本号", "更新人", "时间", "备份地址", "线上地址", "注释"])
        x.padding_width = 1

        for i in history_list:
            x.add_row(i)
        print(x)


def handler(signal_num, frame):
    print "\n程序终止"
    sys.exit(signal_num)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    s = View()
    s.start()
