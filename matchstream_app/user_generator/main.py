import time
from generator.user_generator import UserGenerator
from kafka_producer.kafka_producer import UserKafkaProducer
from utils.serializer import user_to_dict

def run():
    generator = UserGenerator()
    producer = UserKafkaProducer()

    print("Starting continuous user generation every 2 seconds...\n")

    try:
        while True:
            users = generator.generate_users()

            print(f"\nGenerated {len(users)} users")

            for u in users:
                event = user_to_dict(u)
                producer.send_user_event(event)
                print("Sent to Kafka:", event["user_id"])

            producer.flush()
            print(f"✔ Flushed {len(users)} users to Kafka.")

            time.sleep(2)  # WAIT 2 SECONDS BEFORE NEXT API CALL

    except KeyboardInterrupt:
        print("\nStopping gracefully...")
        producer.flush()
        print("Kafka producer closed.")


if __name__ == "__main__":
    run()