#!/bin/bash
set -e

echo "🔥 Waiting for Kafka Connect REST API..."
until curl -s http://kafka_connect:8083/ > /dev/null; do
  sleep 2
done

echo "✅ Kafka Connect is up."

# Check if connector already exists
if curl -s http://kafka_connect:8083/connectors/pg-writer-cdc | grep '"name"'; then
    echo "⚠️ Connector already exists. Skipping creation."
    exit 0
fi

echo "🚀 Creating Debezium connector..."

curl -X POST \
  -H "Content-Type: application/json" \
  --data @/kafka-connect-config/debezium_writer_to_kafka.json \
  http://kafka_connect:8083/connectors

echo "🎉 Connector created successfully!"