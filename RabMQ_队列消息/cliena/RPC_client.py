#!/usr/bin/env python3
#Created by xuchao on 16/7/25.
import pika,subprocess

RabbitMQ_HOST = '192.168.56.2'
GROUP = 'logs'
WAY = 'fanout'
# 定义主机名,目前是以队列名称区分,如多实例执行请更改38行queue_name为HOSTNAME
HOSTNAME = 'n1'


# 连接rabbitmq服务器
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RabbitMQ_HOST))
channel = connection.channel()


channel.exchange_declare(exchange=GROUP,
                         type=WAY)
# 生成随机队列名称
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

# 绑定队列及组
channel.queue_bind(exchange=GROUP,
                   queue=queue_name)


# 执行命令返回 任务执行结果
def perform(body):
    p = subprocess.Popen(body, stdout=subprocess.PIPE)
    rest = p.stdout.read()
    return rest


# 定义接收到消息的处理方法
def request(ch, method, properties, body):
    print ("cmd (%s)" % (str(body,encoding='utf8')))
    response = '%s\n%s' %(queue_name,perform(str(body, encoding='utf8')).decode())
    # 将计算结果发送回server
    ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     body=response)
# 执行接收消息队列命令
channel.basic_consume(request, queue=queue_name)
# 开始监听任务
channel.start_consuming()