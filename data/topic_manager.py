import subprocess
import time


KAFKA_BOOTSTRAP = "localhost:9092"
KAFKA_BIN = "/home/harshithts/Downloads/Kafka/bin"
def reset_topics(topics):
    print("Resetting Kafka topics")

    # deleete all topics
    for topic in topics:
        print(f"Deleting topic: {topic}")
        subprocess.run([
            f"{KAFKA_BIN}/kafka-topics.sh",
            "--delete",
            "--bootstrap-server", KAFKA_BOOTSTRAP,
            "--topic", topic
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    time.sleep(1)
    for topic in topics:
        print(f"Creating topic: {topic}")
        subprocess.run([
            f"{KAFKA_BIN}/kafka-topics.sh",
            "--create",
            "--bootstrap-server", KAFKA_BOOTSTRAP,
            "--topic", topic,
            "--partitions", "1",
            "--replication-factor", "1"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print("All Kafka topics reset.")
