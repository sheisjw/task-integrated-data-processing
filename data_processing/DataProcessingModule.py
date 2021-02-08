from datetime import datetime
import logging
import sys
import uuid
sys.path.append("../shared_functions")
from function_a import function_a


class DataProcessingModule:
    def __init__(self, consumer, another_producer, topic_b, batch_manager):
        self.consumer = consumer
        self.topic_b = topic_b
        self.another_producer = another_producer
        self.batch_manager = batch_manager
        self.records_list = []

    def consume_records(self):
        try:
            while True:
                # this method returns immediately if there are records available -
                # otherwise, it will await the passed timeout if the timeout expires,
                # an empty record set will be returned (poll is executed, new loop started)
                record = self.consumer.poll(self.batch_manager.poll_interval)

                if record is not None:
                    if record.error():  # error in consumer message
                        logging.error('Consumer error:', {record.error()})
                    else:  # valid non-none message passed
                        self.parse_kafka_message(record)

                        if self.batch_manager.calculate_iteration_boundaries(record.timestamp()[1]):
                            self.finish_micro_batch()
                elif self.batch_manager.calculate_iteration_boundaries_empty():  # no message consumed
                    self.finish_micro_batch()
        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()

    def finish_micro_batch(self):
        def delivery_report(err, msg):
            """ Called once for each message produced to indicate delivery result.
                Triggered by poll() or flush(). """
            if err is not None:
                print('Message processed, but delivery failed: {}'.format(err))
            else:
                print('Message processed, and delivered to {}, key:{}, message: {}'.format(msg.topic(), msg.key(), msg.value()))

        if len(self.records_list) > 0:
            # processed_records_list = [preprocess_text(text.decode('utf-8')) for text in (self.records_list)]
            # since there is no pre-processing required for this example, no data processing module is executed
            processed_records_list = self.records_list
            record_key = str(uuid.uuid4())
            record_value = str(processed_records_list)
            self.another_producer.produce(self.topic_b, key=record_key, value=record_value, on_delivery=delivery_report)
            self.another_producer.poll(0)
            self.another_producer.flush()

            self.records_list.clear()

            self.consumer.commit(asynchronous=False)
        self.batch_manager.commit_iteration_boundaries()

    def parse_kafka_message(self, record):
        record_time = datetime.utcfromtimestamp(record.timestamp()[1] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        print('Received new record at', {record_time})

        self.records_list.append(record.value())
