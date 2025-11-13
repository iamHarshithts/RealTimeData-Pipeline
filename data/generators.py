
import random
from datetime import datetime
from faker import Faker
fake = Faker()
import time
def generate_user_profiles(num_users=10):
    return [
        {
            "user_id": f"U{i:04d}",
            "name": fake.name(),
            "country": fake.country(),
            "account_type": random.choice(["Savings", "Current"]),
            "credit_score": random.randint(300, 850),
            "status": random.choice(["active", "suspended", "closed"]),
            "timestamp": fake.date_time_this_year().isoformat()
        }
        for i in range(1, num_users + 1)
    ]


def generate_merchant_info(num_merchants=10):
    return [
        {
            "merchant_id": f"M{i:04d}",
            "merchant_name": fake.company(),
            "category": random.choice(["E-commerce", "Restaurant", "Fuel", "Travel", "Retail"]),
            "risk_level": random.choice(["Low", "Medium", "High"]),
            "country": random.choice(["USA", "India", "Russia"]),
            "timestamp": fake.date_time_this_year().isoformat()
        }
        for i in range(1, num_merchants + 1)
    ]


def generate_account_balances(user_profiles):
    return [
        {
            "account_id": f"A{i:04d}",
            "user_id": user["user_id"],
            "current_balance": round(random.uniform(1000, 200000), 2),
            "currency": "INR",
            "last_updated": fake.date_time_this_year().isoformat()
        }
        for i, user in enumerate(user_profiles, start=1)
    ]


def generate_transaction(user_profiles, merchant_info):
    user = random.choice(user_profiles)
    merchant = random.choice(merchant_info)

    return {
        "txn_id": f"T{int(time.time() * 1000)}",
        "user_id": user["user_id"],
        "amount": round(random.uniform(100, 50000), 2),
        "merchant_id": merchant["merchant_id"],
        "channel": random.choice(["ATM", "POS", "Online"]),
        "location": fake.city(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
