#!/usr/bin/env python3
#Created by xuchao on 16/7/18.
import threading, time,queue

class ThreadPool:

    def __init__(self,max_num,max_task_num=None):
        """

        :param max_num: 最大线程数
        :param max_task_num: 最大任务数
        :return:
        """
        self.max_num = max_num
        if max_task_num:
            self.q = queue.Queue(max_task_num)
        else:
            self.q = queue.Queue()
        self.thread_list = []             # 线程任务列表
        self.free_list = []                 # 等待任务列表


    def run(self,func,args):
        """
        线程池执行一个任务
        :param func: 任务函数
        :param args: 任务函数所需参数
        :return: 如果线程池已经终止，则返回True否则None
        """
        if len(self.free_list) == 0 and len(self.thread_list) < self.max_num: # 等待任务列表为空 且 线程列表任务数量小于最大线程
            self.generate_thread()      # 执行 generate_thread 方法
        w = (func, args,)               # 传入参数放入元组
        self.q.put(w)                   # 把元组传入 queue 队列

    def generate_thread(self):
        """
        生成线程
        :return:
        """
        t = threading.Thread(target=self.call)
        t.start()

    def call(self):
        current_thread = threading.currentThread    # 获取当前的线程对象（Thread object)
        self.thread_list.append(current_thread)   # 把线程对象添加到线程任务列表
        event = self.q.get()
        while event:
            func, args = event
            func(*args)
            event = self.q.get()


pool = ThreadPool(5)

# 具体要做的任务
def action_1(args):
    print(threading.current_thread(),'任务一',args)  # 打印线程以确定是否是一个线程
    time.sleep(0.5) # 模拟执行时间

def action_2(args):
    print(threading.current_thread(),'任务二',args)  # 打印线程以确定是否是一个线程
    time.sleep(0.5) # 模拟执行时间


# 执行次数
for i in range(30):
    pool.run(action_1, (i,))
    pool.run(action_2, (i,))
