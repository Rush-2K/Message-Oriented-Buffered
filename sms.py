import http.client
from pandas import array
import pika, time, json

phone = []

# method to send the sms
def sms_function(msg):
    msg = json.loads(msg)
    message = msg['msg']
    for x in phone:
      conn = http.client.HTTPSConnection("api.sms.to")
      payload = "{\n    \"message\": \""+message+"\",\n    \"to\": \" "
      str1 = payload+x+"\",\n    \"sender_id\": \"hazieq\"    \n}"
      headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2F1dGg6ODA4MC9hcGkvdjEvdXNlcnMvYXBpL2tleS9nZW5lcmF0ZSIsImlhdCI6MTY1NDkzODUzMSwibmJmIjoxNjU0OTM4NTMxLCJqdGkiOiJoRGVScDhyOVZnMDBUSFVIIiwic3ViIjozODA4NTEsInBydiI6IjIzYmQ1Yzg5NDlmNjAwYWRiMzllNzAxYzQwMDg3MmRiN2E1OTc2ZjcifQ.djYvghsjtRHNWVnyncgyIpwxdoBqO3jTm0ztscenIaI'
      }
      conn.request("POST", "/sms/send", str1, headers)
      res = conn.getresponse()
      data = res.read()
      print(data.decode("utf-8"))

def call(arr):
  # set credentials parameters
  global phone
  phone = arr
  credentials = pika.PlainCredentials('guest', 'guest')
  parameters = pika.ConnectionParameters('localhost',
                                    5672,
                                    'shaeri-vc',
                                    credentials)

  # create connection
  connection = pika.BlockingConnection(parameters)
  # create channel
  channel = connection.channel()

  # create single active queue if it is not already created
  channel.queue_declare(queue='subscriber_SMS', arguments = {"x-single-active-consumer": True})
  # bind the queue to new_registration exchange
  channel.queue_bind(exchange='new_registration', queue='subscriber_SMS')

  def callback(ch, method, properties, body):
    sms_function(body)

  # set up subscription on the queue
  channel.basic_consume('subscriber_SMS',
    callback,
    auto_ack=True)

  # start listening to the queue (blocks)
  channel.start_consuming()
  connection.close()