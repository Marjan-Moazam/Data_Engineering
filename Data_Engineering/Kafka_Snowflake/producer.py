from confluent_kafka import Producer
import requests
import json
import time

# Kafka config
p = Producer({"bootstrap.servers": "localhost:9092"})


def delivery_report(err, msg):
    if err:
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"✅ Message delivered to {msg.topic()} [{msg.partition()}]")


def fetch_all_carts():
    url = "https://fakestoreapi.com/carts"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("❌ Failed to fetch carts")
        return []


# Fetch all carts and send each one to Kafka
all_carts = fetch_all_carts()

for cart in all_carts:
    p.produce("fakestore_purchases", json.dumps(cart), callback=delivery_report)
    p.flush()
    time.sleep(0.5)  # optional delay between sends
