#!/usr/bin/env python3
#Created by xuchao on 16/7/25.
import pika,time
HOST = '192.168.56.2'
GROUP = 'logs'
WAY = 'fanout'
TIME = 5
COMMONS = 'ls'

class Center(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=HOST))

        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=GROUP,
                                 type=WAY)

        # 定义接收返回消息的队列
        result = self.channel.queue_declare(exclusive=True)
        # 随机队列名称
        self.callback_queue = result.method.queue
        # 添加 接收返回消息
        self.channel.basic_consume(self.callback,
                                   no_ack=True,
                                   queue=self.callback_queue)

    # 定义接收到返回消息的处理方法
    def callback(self, ch, method, props, body):
        # self.response = body
        print(body.decode())

    def request(self, n):
        self.response = None
        #发送计算请求，并声明返回队列 # reply_to 返回队列名称
        self.channel.basic_publish(exchange=GROUP,
                                   routing_key=self.callback_queue,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,),
                                   body=str(n))
        # 设定接收时间
        Nowtime = time.time() + TIME
        while time.time() < Nowtime:
            # 接收返回的数据,等待返回数据
            self.connection.process_data_events()
        # return self.response
        # self.channel.start_consuming()

center = Center()

response = center.request(COMMONS)
