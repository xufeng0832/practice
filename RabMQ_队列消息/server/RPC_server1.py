#!/usr/bin/env python3
#Created by xuchao on 16/7/25.
import pika,hashlib,time,json
import sys


class My_RPC_server:

    def __init__(self, mq_host, exchange=None, type='fanout', routing_key=''):
        """

        :param mq_host: rabbitme服务地址
        :param exchange: 队列组名称
        :param type: 发送模式
        :param routing_key: 队列名
        :return:
        """
        # 绑定端口
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=mq_host))
        # 创建消息队列
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        # 随机队列名称
        self.callback_queue = result.method.queue

        self.exchange = exchange
        self.type = type
        self.routing_key = routing_key
    # 设置组名
    def __group(self):
        # exchange 绑定队列组 type 是队列指定的类型 fanout 是所有队列都发送
        self.channel.exchange_declare(exchange=self.exchange,type=self.type)
    # 设置队列名
    def __single(self):
        self.channel.queue_declare(queue=self.callback_queue)

    #  发送消息
    def __message(self,ms):
        host = md5sum()
        message = json.dumps((host,ms))
        # 往logs 组发送消息  body 发送的信息
        self.channel.basic_publish(exchange=self.exchange,
                              routing_key=self.callback_queue,
                              body=message)

        # 关闭 rabbitmq 连接    (pika)
        self.connection.close()

        clinea_boj = My_RPC_server('192.168.56.2', routing_key=host)
        clinea_boj.__recv_message()

    def callback(self,ch, method, properties, body):
        print(str(body,encoding='utf8'))


    def __recv_message(self):
        # self.__single()
        self.channel.basic_consume(self.callback,queue=self.callback_queue,no_ack=True)
        self.channel.start_consuming()
        self.connection.close()




    def run(self,message):
        if self.exchange:
            self.__group()
        # if self.routing_key:
        #     self.__single()
        self.__message(message)


def md5sum():
    hash = hashlib.md5()
    hash.update(bytes(str(time.time()),encoding='utf8'))
    return hash.hexdigest()


obj = My_RPC_server('192.168.56.2', 'logs', routing_key='xuchao')

obj.run('ls')