#!/usr/bin/env python3
#Created by xuchao on 16/7/18.
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import queue
import threading
import contextlib
import time

StopEvent = object()


class ThreadPool(object):

    def __init__(self, max_num, max_task_num = None):
        """

        :param max_num: 最大线程数
        :param max_task_num: 最大任务数
        :return:
        """
        if max_task_num:
            self.q = queue.Queue(max_task_num)
        else:
            self.q = queue.Queue()
        self.max_num = max_num
        self.cancel = False
        self.terminal = False
        self.generate_list = []             # 线程任务列表
        self.free_list = []                 # 等待任务列表

    def run(self, func, args, callback=None):
        """
        线程池执行一个任务
        :param func: 任务函数
        :param args: 任务函数所需参数
        :param callback: 任务执行失败或成功后执行的回调函数，回调函数有两个参数1、任务函数执行状态；2、任务函数返回值（默认为None，即：不执行回调函数）
        :return: 如果线程池已经终止，则返回True否则None
        """
        if self.cancel:
            return
        if len(self.free_list) == 0 and len(self.generate_list) < self.max_num: # 等待任务列表为空 且 线程列表任务数量小于最大线程
            self.generate_thread()      # 执行 generate_thread 方法
        w = (func, args, callback,)     # 传入参数放入元组
        self.q.put(w)                   # 把元组传入 queue 队列

    def generate_thread(self):
        """
        创建一个线程
        """
        t = threading.Thread(target=self.call)      # 传入 self.call 方法
        t.start()                                   # 执行 call方法

    def call(self):
        """
        循环去获取任务函数并执行任务函数
        """
        current_thread = threading.currentThread    # 获取当前的线程对象（Thread object)
        self.generate_list.append(current_thread)   # 把线程对象添加到线程任务列表

        event = self.q.get()                        # 取出 queue 队列的参数
        while event != StopEvent:                   # event 不是空

            func, arguments, callback = event       # 拆解元组
            try:
                result = func(*arguments)           # 执行方法
                success = True
            except Exception as e:
                success = False
                result = None

            if callback is not None:                # 如果回调方法不是空
                try:
                    callback(success, result)       # 执行回调方法 把线程执行结果 及 执行后的返回值传入
                except Exception as e:
                    pass
            # print(self.free_list)
            # print(current_thread)
            # print(threading.current_thread())
            with self.worker_state(self.free_list, current_thread):     # 执行 worker_state 方法
                if self.terminal:
                    event = StopEvent
                else:
                    event = self.q.get()                                # 取出 queue 的下一个任务
        else:

            self.generate_list.remove(current_thread)

    def close(self):
        """
        执行完所有的任务后，所有线程停止
        """
        self.cancel = True
        full_size = len(self.generate_list)
        while full_size:
            self.q.put(StopEvent)
            full_size -= 1

    def terminate(self):
        """
        无论是否还有任务，终止线程
        """
        self.terminal = True

        while self.generate_list:
            self.q.put(StopEvent)

        self.q.empty()

    @contextlib.contextmanager
    def worker_state(self, state_list, worker_thread):
        """
        用于记录线程中正在等待的线程数
        """
        state_list.append(worker_thread)
        try:
            yield
        finally:
            state_list.remove(worker_thread)



# How to use


pool = ThreadPool(5)

def callback(status, result):
    # status, execute action status
    # result, execute action return value
    pass


def action(i):
    time.sleep(1)
    print(i)

for i in range(30):
    ret = pool.run(action, (i,), callback)

time.sleep(7)
print(len(pool.generate_list), len(pool.free_list))
print(len(pool.generate_list), len(pool.free_list))
# pool.close()
# pool.terminate()