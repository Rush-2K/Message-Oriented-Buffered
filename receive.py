import pika, time, json, smtplib, ssl
import requests
from sklearn.metrics import adjusted_rand_score
from sms import call

api = requests.get('http://127.0.0.1:5000/api/v1')
api = api.json()
index = 0

# send email method
def email_function(msg):
  global index
  print(" Email service started")
  arr = []
  [arr.append(api[x]['email']) for x in range(len(api))]
  #Convert the serialized messaged to Python dictionary
  print(" [x] Sending Email to " , arr)
  port = 465  # For SSL
  smtp_server = "smtp.gmail.com"
  # need to use your email and password
  sender_email = ''
  password = ""
  msg = json.loads(msg)
  message = msg['msg']
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)            #login
    server.sendmail(sender_email, arr, message)     #send email

  time.sleep(5) # delays for 5 seconds
  print(" Email service finished")
  index = index + 1
  return

# set credentials parameters
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost',
                                   5672,
                                   'shaeri-vc',
                                   credentials)

# create connection
connection = pika.BlockingConnection(parameters)
# create channel
channel = connection.channel()

def callback(ch, method, properties, body):
  email_function(body)
  arr = []
  [arr.append(api[x]['phone_number']) for x in range(len(api))]
  # call the sms function
  call(arr)

queue_name = 'subscriber_email'
# create a queue based on the user email
channel.queue_declare(queue=queue_name, exclusive=False)
# create a relationship between exchange and a queue
channel.queue_bind(exchange='new_registration', queue=queue_name)
# tell RabbitMQ that this particular callback function should receive messages from our queue
channel.basic_consume(queue=queue_name, 
  on_message_callback=callback, 
  auto_ack=True)

# start listening to the queue (blocks)
channel.start_consuming()
# connection.close()