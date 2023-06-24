import pika
import ftchat.applicationConf as applicationConf

def callback(ch, method, properties, body):
    print(f"Received message: {body}")

def process_message():

    connection = pika.BlockingConnection(pika.ConnectionParameters(applicationConf.rabbitmq_host,
                                                                credentials=pika.PlainCredentials('Boojux',
                                                                                                    'BoojuxRabbitMQ')
                                                                ))

    channel = connection.channel()

    channel.basic_consume(queue='ftchat.friend.add', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
