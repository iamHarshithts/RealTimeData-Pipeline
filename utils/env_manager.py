def adding_bucket_to_env(bucket_name):
    import os
    env_path = './.env'
    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()

    lines = [line for line in lines if not line.startswith("BUCKET_NAME=")]
    lines.append(f"BUCKET_NAME={bucket_name}\n")

    with open(env_path, "w") as f:
        f.writelines(lines)

    print(f"Bucket name '{bucket_name}' added to .env")
