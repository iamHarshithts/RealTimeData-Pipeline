from config.kafka_config import get_consumer
from config.s3_config import get_s3_client
from kafka import KafkaConsumer
from core.signals import users_done, merchants_done, balances_done
import json

def consume_user_profiles(total,bucketName):
    s3 = get_s3_client()
    consumer = KafkaConsumer(
        'user_profiles',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    count = 0
    for msg in consumer:
        data = msg.value
        key = f"bronze/profiles-folder/{data['user_id']}.json"
        s3.put_object(Bucket=bucketName, Key=key, Body=json.dumps(data))
        print(f"Uploaded user → {key}")

        count += 1
        if count >= total:
            print("All user profiles uploaded.")
            users_done.set()
            return  


def consume_merchants(total,bucketName):
    users_done.wait()

    s3 = get_s3_client()
    consumer = KafkaConsumer(
        'merchant_info',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    count = 0
    for msg in consumer:
        data = msg.value
        key = f"bronze/merchant-folder/{data['merchant_id']}.json"
        s3.put_object(Bucket=bucketName, Key=key, Body=json.dumps(data))
        print(f"Uploaded merchant → {key}")

        count += 1
        if count >= total:
            print("All merchant info uploaded.")
            merchants_done.set()
            return


def consume_account_balances(total,bucketName):

    merchants_done.wait()

    s3 = get_s3_client()
    consumer = KafkaConsumer(
        'account_balances',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    count = 0
    for msg in consumer:
        data = msg.value
        key = f"bronze/account-folder/{data['account_id']}.json"
        s3.put_object(Bucket=bucketName, Key=key, Body=json.dumps(data))
        print(f"Uploaded account balance → {key}")

        count += 1
        if count >= total:
            print("All account balances uploaded.")
            balances_done.set()
            return


def consume_transactions(bucketName):

    balances_done.wait()

    s3 = get_s3_client()
    consumer = KafkaConsumer(
        'transactions',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    for msg in consumer:
        data = msg.value
        key = f"bronze/transactions-folder/{data['txn_id']}.json"
        s3.put_object(Bucket=bucketName, Key=key, Body=json.dumps(data))
        print(f"Uploaded transaction → {key}")

