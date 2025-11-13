from config.kafka_config import producer
from data.generators import generate_transaction
from core.signals import balances_done
import time
def produce_transactions(user_profiles, merchant_info):
    balances_done.wait()
    print("✅ Starting transaction generation...")
    for _ in range(100):
        txn = generate_transaction(user_profiles, merchant_info)
        producer.send("transactions", value=txn)
        producer.flush()
        print(f"✅ Sent transaction → {txn['txn_id']}")
        time.sleep(1)
    print("✅ Transaction generation completed.")
