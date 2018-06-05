#_*_coding:utf-8_*_
import pika
import time
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='rpc_q')

def hello(n):
#    if n == 0:
#        return 0
#    elif n == 1:
#        return 1
#    else:
#       return hello(n-1) + hellon-2)
    z = n + n
    return z

def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] hello(%s)" % n)
    response = hello(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                   props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(on_request, queue='rpc_q')

print(" [x] Awaiting RPC requests")
channel.start_consuming()
