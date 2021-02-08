import argparse
from confluent_kafka import Consumer, Producer
from BatchManager import BatchManager
from DataProcessingModule import DataProcessingModule

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--broker')
    parser.add_argument('--source_topic')
    parser.add_argument('--group_id')
    parser.add_argument('--batch_interval_seconds')
    parser.add_argument('--poll_interval_seconds')
    parser.add_argument('--target_topic')
    args = parser.parse_args()

    # create Batch Manager with certain batch duration
    batch_manager = BatchManager(int(args.batch_interval_seconds), int(args.poll_interval_seconds))

    # create Kafka Consumer
    consumer = Consumer({'bootstrap.servers': args.broker,
                         'group.id': args.group_id,
                         'auto.offset.reset': 'earliest',
                         'enable.auto.commit': False})
    consumer.subscribe([args.source_topic])

    another_producer = Producer({'bootstrap.servers': args.broker})

    batch_consumer = DataProcessingModule(consumer, another_producer, args.target_topic, batch_manager)
    batch_consumer.consume_records()

# python process_data.py --broker kafka:9092 --source_topic topic_a --group_id my-group --batch_interval_seconds 30 --poll_interval_seconds 10 --target_topic=topic_b
