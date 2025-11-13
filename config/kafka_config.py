import json
KAFKA_BOOTSTRAP = "localhost:9092"


from kafka import KafkaProducer, KafkaConsumer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def get_consumer(topic):
    return KafkaConsumer(
        topic,
        bootstrap_servers=[KAFKA_BOOTSTRAP],
        auto_offset_reset='earliest',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
