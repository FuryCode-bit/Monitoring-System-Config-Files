# Consumidor de Temperatura em Fahrenheit
from flask import Flask, jsonify
import pika
import threading

app = Flask(__name__)
temperature_fahrenheit = None

def consume_fahrenheit():
    global temperature_fahrenheit
    connection = pika.BlockingConnection(pika.ConnectionParameters('0.0.0.0'))
    channel = connection.channel()
    channel.exchange_declare(exchange='temperature_exchange', exchange_type='topic')

    queue = channel.queue_declare(queue='temperature_queue', exclusive=False)
    queue_name = queue.method.queue

    channel.queue_bind(exchange='temperature_exchange', queue=queue_name, routing_key='temperature.fahrenheit')

    def callback(ch, method, properties, body):
        global temperature_fahrenheit
        temperature_fahrenheit = float(body)
        print(f"Updated Fahrenheit temperature: {temperature_fahrenheit}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

@app.route('/', methods=['GET'])
def get_temperature_fahrenheit():
    return jsonify({"temperature": temperature_fahrenheit, "unit": "Fahrenheit"})

if __name__ == '__main__':
    threading.Thread(target=consume_fahrenheit, daemon=True).start()
    app.run(host='0.0.0.0', port=5005, debug=True)