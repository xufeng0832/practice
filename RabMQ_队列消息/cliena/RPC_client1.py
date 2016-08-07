#!/usr/bin/env python3
#Created by xuchao on 16/7/25.
import pika,json,subprocess

# 绑定 rabbitmq
class My_RPC_cliena:
    def __init__(self, mq_host, exchange=None, type='fanout'):
        """

        :param mq_host: MQ 队列地址
        :param exchange: 队列组名称
        :return:
        """
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=mq_host))
        self.channel = self.connection.channel()     # 创建一个频道
        self.exchange = exchange                # 定义queue组
        self.type = type                        # 定义发送方式
        self.channel.exchange_declare(exchange=self.exchange,type=self.type)
        self.q_name = True                      # 标志位是否设置队列名

    def __group(self):
        """
        创建一个队列组 指定组名 和 队列类型  (有则创建,无则pass)
        :return:
        """

        # 创建一个随机队列
        self.result = self.channel.queue_declare(exclusive=True)
        self.queue_name = self.result.method.queue

    # 创建随机队列名
    def __single(self):
        self.queue_name = self.result.method.queue


    def specified_single(self,Queue_name):
        """
        指定队列名
        :param Queue_name: str
        :return:
        """
        self.queue_name = Queue_name
        self.q_name = False

    def __bind_queue(self):
        """
        频道绑定 指定队列组 和 队列名
        :return:
        """
        if self.q_name:
            self.__group()
            self.__single()
        self.channel.queue_bind(exchange=self.exchange,
                           queue=self.queue_name)


    def __callback(self,ch, method, properties, body):
        date = json.loads(str(body,encoding='utf8'))
        print(date)
        p =subprocess.Popen(date[1],stdout=subprocess.PIPE)
        rest = p.stdout.read()

        server_obj = My_RPC_cliena('192.168.56.2',)
        server_obj.__send_message(date[0], str(rest,encoding='utf8'))

    def __send_message(self, routing_key, message):
        self.channel.queue_declare(queue='hello')

        self.channel.basic_publish(exchange='',
                                   routing_key=routing_key,
                                   body=message)
        self.connection.close()

    def run(self):
        self.__bind_queue()
        self.channel.basic_consume(self.__callback,
                              queue=self.queue_name,
                              no_ack=True)
        self.channel.start_consuming()


obj = My_RPC_cliena('192.168.56.2', 'logs')
# obj.specified_single('xuchao')
obj.run()