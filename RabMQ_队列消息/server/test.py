#!/usr/bin/env python3
#Created by xuchao on 16/7/29.



server='服务端'

"""
import pika,time

HOST = '192.168.56.2'
# QUEUE = 'queue'

class Center(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=HOST))

        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='logs',
                                 type='fanout')

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
        self.channel.basic_publish(exchange='logs',
                                   routing_key=self.callback_queue,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,),
                                   body=str(n))
        # 设定接收时间
        Nowtime = time.time()+5
        while time.time() < Nowtime:
            # 接收返回的数据,等待返回数据
            self.connection.process_data_events()
        # return self.response
        # self.channel.start_consuming()

center = Center()

response = center.request('ls')
"""


client = '客户端'
'''
import pika,subprocess

HOST = '192.168.56.2'
# QUEUE = 'queue'

# 连接rabbitmq服务器
connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
channel = connection.channel()


channel.exchange_declare(exchange='logs',
                         type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

# # 定义队列
# channel.queue_declare(queue=QUEUE)
channel.queue_bind(exchange='logs',
                   queue=queue_name)


# 执行命令返回 任务执行结果
def perform(body):
    p = subprocess.Popen(body, stdout=subprocess.PIPE)
    rest = p.stdout.read()
    return rest


# 定义接收到消息的处理方法
def request(ch, method, properties, body):
    print ("cmd (%s)" % (str(body,encoding='utf8')))
    # response = '%s\n%s' %(queue_name,str(perform(str(body, encoding='utf8'))))
    # ret = str(perform(str(body, encoding='utf8')))
    # print(ret)
    response = '%s\n%s' %(queue_name,perform(str(body, encoding='utf8')).decode())
    # print(response)
    # response = perform(str(body, encoding='utf8'))
    # 将计算结果发送回server
    ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     body=response)
    # ch.basic_ack(delivery_tag=method.delivery_tag)

# channel.basic_qos(prefetch_count=1)
# 执行接收消息队列命令
channel.basic_consume(request, queue=queue_name)
# 开始监听任务
channel.start_consuming()
'''