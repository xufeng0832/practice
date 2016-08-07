#!/usr/bin/env python3
#Created by xuchao on 16/7/18.
import queue
import threading
import time


class WorkManager:

    def __init__(self, jobs, args, work_num=1000, thread_num=2):
        self.work_queue = queue.Queue()     # 工作队列对象
        self.threads = []                   # 线程列表
        self.jobs = jobs                    # 执行的任务
        self.args = args
        self.__init_work_queue(work_num)    # 把工作加入队列
        self.__init_thread_pool(thread_num) # 开启线程数量

    def __init_thread_pool(self,thread_num):
        """
        初始化线程池
        :param thread_num:最大工作线程数
        :return:
        """
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue,self.threads))

    def __init_work_queue(self, jobs_num):
        """
        初始化工作队列
        :param jobs_num: 工作次数
        :return:
        """
        for i in range(jobs_num):
            self.add_job(self.jobs, self.args)

    def add_job(self, func, *args):
        """
        添加一项工作入队
        :param func: 任务(函数)
        :param args: 第几个任务
        :return:
        """
        self.work_queue.put((func, list(args))) # 任务入队，Queue内部实现了同步机制

    def wait_all_complete(self):
        """
        等待所有线程运行完毕
        :return:
        """
        for item in self.threads:
            if item.isAlive():          # 判断线程是否是激活的（alive）
                item.join()             # 调用Thread.join将会使主调线程堵塞，直到被调用线程运行结束。

class Work(threading.Thread):
    def __init__(self, work_queue, threads):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.threads = threads
        self.start()

    def run(self):
        # 死循环，从而让创建的线程在一定条件下关闭退出
        while True:
            try:
                if self.work_queue.empty() and len(self.threads) > 5:
                    do, args = self.work_queue.get(block=False) # 任务异步出队，队列为空报错。
                else:
                    do, args = self.work_queue.get()
                do(args)
                self.work_queue.task_done() # 通知系统任务完成
            except:
                """
                是否持续保持线程存在
                """
                # self.threads.remove(threading.current_thread())
                # print('The destruction',threading.current_thread())
                break

# 具体要做的任务
def do_job(args):
    time.sleep(0.1) # 模拟处理时间
    print (threading.current_thread(), list(args))

if __name__ == '__main__':
    start = time.time()
    work_manager =  WorkManager(do_job,1,100, 10) # 或者work_manager =  WorkManager(10000, 20)
    work_manager.wait_all_complete()
    end = time.time()
    print ("cost all time: %s" % (end-start))