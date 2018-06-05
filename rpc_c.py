import pika
import uuid
import time

class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None

        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_q',
                                   properties=pika.BasicProperties(

                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
            print("wait...")
            time.sleep(0.5)
        return int(self.response)
#    def finish(self,response):
#       z = response + response
#       return self.z
#    finish()

fibonacci_rpc = FibonacciRpcClient()

print(" [start] Requesting hello(3)")
response = fibonacci_rpc.call(3)
print(" [finish] Got %r" % response)
print(response)
def finish(n,re):
#   re = fibonacci_rpc.call(3)
    z = re+n
    print ('%s sucess' %z)
    return z
finish(1,response)

