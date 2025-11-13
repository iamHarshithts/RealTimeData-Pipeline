import threading
from data.generators import generate_user_profiles, generate_merchant_info, generate_account_balances
from data.topic_manager import reset_topics
from core.producer import produce_transactions
from core.consumer import (
    consume_user_profiles,
    consume_merchants,
    consume_account_balances,
    consume_transactions
)
from config.s3_config import get_s3_client
from utils.env_manager import adding_bucket_to_env

def create_bucket():
    s3 = get_s3_client()
    bucketName = input("Enter the bucket name: ").strip().lower().replace(" ", "-")
    try:
        # Validate bucket name manually (basic check)
        if not all(c.isalnum() or c in "-." for c in bucketName):
            raise ValueError("❌ Invalid bucket name! Use only lowercase letters, numbers, hyphens, or dots.")
        existing_buckets = [b['Name'] for b in s3.list_buckets().get('Buckets', [])]
        if bucketName not in existing_buckets:
            s3.create_bucket(Bucket=bucketName)
            print(f"✅ Created new bucket: {bucketName}")
        else:
            print(f"🪣 Bucket '{bucketName}' already exists. Using it.")
    except Exception as e:
        if "BucketAlreadyOwnedByYou" in str(e):
            print(f"🪣 Bucket '{bucketName}' already exists. Using it.")
        else:
            print(f"⚠️ Error checking/creating bucket: {e}")
    return bucketName



if __name__ == "__main__":
    topics = [
        "user_profiles",
        "merchant_info",
        "account_balances",
        "transactions"
    ]
    reset_topics(topics)
    bucket_name = create_bucket()
    adding_bucket_to_env(bucket_name)

    users = generate_user_profiles()
    merchants = generate_merchant_info()
    balances = generate_account_balances(users)

    from config.kafka_config import producer
    for u in users:
        producer.send("user_profiles", value=u)
    for m in merchants:
        producer.send("merchant_info", value=m)
    for b in balances:
        producer.send("account_balances", value=b)
    producer.flush()
    print("✅ All static data sent to Kafka")

    threading.Thread(target=consume_user_profiles, args=(len(users), bucket_name), daemon=True).start()
    threading.Thread(target=consume_merchants, args=(len(merchants), bucket_name), daemon=True).start()
    threading.Thread(target=consume_account_balances, args=(len(balances), bucket_name), daemon=True).start()
    threading.Thread(target=consume_transactions, args=(bucket_name,), daemon=True).start()
    threading.Thread(target=produce_transactions, args=(users, merchants), daemon=True).start()

    input("Press Enter to stop...\n")
