import time, logging
from generator.user_generator import UserGenerator
from kafka_producer.kafka_producer import UserKafkaProducer
from utils.serializer import user_to_dict


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def run():
    generator = UserGenerator()
    producer = UserKafkaProducer()

    logger.info("Starting continuous user generation...")

    while True:
        users = generator.generate()
        for user in users:
            event = user_to_dict(user)
            producer.send(event)
        producer.flush()
        logger.info(f"Batch sent to Kafka. Size: {len(users)}")
        time.sleep(2)

if __name__ == "__main__":
    run()