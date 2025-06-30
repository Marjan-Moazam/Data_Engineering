from confluent_kafka import Consumer
import json
import snowflake.connector

# Kafka consumer config
c = Consumer(
    {
        "bootstrap.servers": "localhost:9092",
        "group.id": "fakestore_group",
        "auto.offset.reset": "earliest",
        "session.timeout.ms": 60000,
        "max.poll.interval.ms": 300000,
    }
)
c.subscribe(["fakestore_purchases"])

# Snowflake connection
conn = snowflake.connector.connect(
    user="***",
    password="***",
    account="***",
    warehouse="***",
    database="***",
    schema="***",
)
cursor = conn.cursor()

print("⏳ Waiting for messages...")

try:
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("❌ Kafka Error:", msg.error())
            continue

        print("✅ Received:", msg.value().decode("utf-8"))
        record = json.loads(msg.value())

        # Insert into Snowflake
        cursor.execute(
            """
            INSERT INTO fakestore_purchases(id, userId, date, products)
            SELECT %s, %s, %s, PARSE_JSON(%s)
            """,
            (
                record["id"],
                record["userId"],
                record["date"],
                json.dumps(record["products"]),
            ),
        )
        conn.commit()

except KeyboardInterrupt:
    print("🛑 Consumer stopped by user.")

finally:
    cursor.close()
    conn.close()
    c.close()
