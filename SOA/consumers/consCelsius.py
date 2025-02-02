# Consumidor de Temperatura em Celsius
from flask import Flask, jsonify
import pika
import threading

app = Flask(__name__)
temperature_celsius = None

def consume_celsius():
    global temperature_celsius
    connection = pika.BlockingConnection(pika.ConnectionParameters('0.0.0.0'))
    channel = connection.channel()
    channel.exchange_declare(exchange='temperature_exchange', exchange_type='topic')

    queue = channel.queue_declare(queue='temperature_queue', exclusive=False)
    queue_name = queue.method.queue

    channel.queue_bind(exchange='temperature_exchange', queue=queue_name, routing_key='temperature.celsius')

    def callback(ch, method, properties, body):
        global temperature_celsius
        temperature_celsius = float(body)
        print(f"Updated Celsius temperature: {temperature_celsius}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

@app.route('/', methods=['GET'])
def get_temperature_celsius():
    return jsonify({"temperature": temperature_celsius, "unit": "Celsius"})

if __name__ == '__main__':
    threading.Thread(target=consume_celsius, daemon=True).start()
    app.run(host='0.0.0.0', port=5004, debug=True)