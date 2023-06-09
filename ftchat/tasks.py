import pika
import ftchat.applicationConf as applicationConf
import ftchat.service.account as account_service

def callback(ch, method, properties, body):
    print(f"Received message: {body}")
    account_service.save_contact_request(uid=body.requester,
                                         target = body.requestee,
                                         message=body.message
                                         )

def process_message():

    connection = pika.BlockingConnection(pika.ConnectionParameters(applicationConf.rabbitmq_host,
                                                                credentials=pika.PlainCredentials('Boojux',
                                                                                                    'BoojuxRabbitMQ')
                                                                ))

    channel = connection.channel()

    channel.basic_consume(queue='ftchat.friend.add', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
