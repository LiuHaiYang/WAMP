import  pika
username = 'admin'   #指定远程rabbitmq的用户名密码
pwd = 'admin'
user_pwd = pika.PlainCredentials(username, pwd)
connection =pika.BlockingConnection(pika.ConnectionParameters(host='172.16.100.189', credentials=user_pwd))
channel =connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello world!  ocean')

print('[ocean] Sent Hello World!')
connection.close()