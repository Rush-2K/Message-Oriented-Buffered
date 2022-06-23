<?php
// require('db.php');
require_once 'vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Exchange\AMQPExchangeType;
use PhpAmqpLib\Message\AMQPMessage;

// read message/news
$myfile = fopen("message.txt", "r") or die("Unable to open file!");
$inputJSON = '{"msg":'.'"'.fread($myfile,filesize("message.txt")).'"'.'}';
echo $inputJSON;

// decode JSON
$user_object= json_decode( $inputJSON );
var_dump($user_object);

// set RabbitMQ client parameters
$exchange = "new_registration";
$vhost = "shaeri-vc";
$rabbitmq_username = "guest";
$rabbitmq_password = "guest";
// create a connection to RabbitMQ
$connection = new AMQPStreamConnection('localhost', 5672, $rabbitmq_username, $rabbitmq_password, $vhost);

// Create a Channel on the existing connection
$channel = $connection->channel();

// serialize the user object 
$messageBody = json_encode($user_object);
// echo $messageBody;
// Prepare the message
$message = new AMQPMessage($messageBody,
                          array('content_type' => 'application/json',
                                'delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT));
// send the message to RabbitMQ
$channel->basic_publish($message, $exchange);
 
//Close the Channel & Connection
$channel->close();
$connection->close();

// return result to client
header('Content-Type: application/json; charset=utf-8');
echo "{'result':'OK'}";

?>