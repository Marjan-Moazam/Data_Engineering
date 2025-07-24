
# 🛍️ Kafka Producer-Consumer Pipeline with Snowflake Sink

This project demonstrates a simple **data pipeline** that fetches semi-real e-commerce data from [FakeStoreAPI](https://fakestoreapi.com/), pushes it to a **Kafka topic**, and consumes it into a **Snowflake** data warehouse.

---

## 🔧 Components

### 1. Producer

- **Script:** `producer.py`
- **Source:** Fetches cart data from FakeStoreAPI (`/carts` endpoint)
- **Kafka Topic:** `fakestore_purchases`
- **Library:** `confluent_kafka`

Each cart object (including user ID, date, and products) is serialized to JSON and published to Kafka.

### 2. Consumer

- **Script:** `consumer.py`
- **Kafka Topic:** Subscribes to `fakestore_purchases`
- **Target:** Inserts JSON records into a Snowflake table
- **Insert Strategy:** Uses `PARSE_JSON` to insert product list

---

## 🧰 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

Dependencies:
- `requests`
- `confluent_kafka`
- `snowflake-connector-python`

---

## ▶️ How to Run

### Step 1: Start Kafka

Use `docker-compose` to spin up Kafka locally:

```bash
docker-compose up -d
```

### Step 2: Run the Producer

```bash
python producer.py
```

This fetches data from the FakeStoreAPI and produces messages to Kafka.

### Step 3: Run the Consumer

```bash
python consumer.py
```

This listens for messages and inserts them into Snowflake.

> 🔐 Make sure to update your Snowflake credentials in `consumer.py` before running.

---

## 🧪 Sample Data Format

A single message looks like:

```json
{
  "id": 1,
  "userId": 1,
  "date": "2020-03-02T00:00:00.000Z",
  "products": [
    { "productId": 1, "quantity": 4 },
    { "productId": 2, "quantity": 1 },
    { "productId": 3, "quantity": 6 }
  ]
}
```

---

## 🏁 Table Schema in Snowflake

Ensure your target table exists in Snowflake:

```sql
CREATE TABLE fakestore_purchases (
  id INT,
  userId INT,
  date TIMESTAMP,
  products VARIANT
);
```

---

## 📎 Notes

- This setup is suitable for learning and prototyping.
- Replace FakeStoreAPI with your own e-commerce data source for production use.
- Add retry logic and error handling for real-world robustness.

---

## 👨‍💻 Author

Built with ❤️ by Marjan Moazam
