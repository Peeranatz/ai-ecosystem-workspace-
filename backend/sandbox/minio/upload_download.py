import os
from minio import Minio
from core.config import settings

def run_upload_download_demo():
    print("=== 1. Connecting to MinIO Client ===")
    client = Minio(
        endpoint=settings.minio_endpoint,
        access_key=settings.minio_root_user,
        secret_key=settings.minio_root_password,
        secure=False
    )
    print(f"Connected to MinIO at {settings.minio_endpoint}")

    bucket_name = settings.minio_bucket
    print(f"\n=== 2. Checking Bucket: '{bucket_name}' ===")
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' created successfully.")
    else:
        print(f"Bucket '{bucket_name}' already exists.")

    # Create dummy file to upload
    local_upload_file = "sandbox/minio/sample_upload.txt"
    os.makedirs(os.path.dirname(local_upload_file), exist_ok=True)
    with open(local_upload_file, "w", encoding="utf-8") as f:
        f.write("Hello MinIO! This is a test file for Assignment 05 upload/download demo.\n")

    object_name = "test_profile_data.txt"
    print(f"\n=== 3. Uploading file '{local_upload_file}' to object '{object_name}' ===")
    client.fput_object(
        bucket_name=bucket_name,
        object_name=object_name,
        file_path=local_upload_file,
    )
    print("Upload completed successfully!")

    # Download file
    local_download_file = "sandbox/minio/downloaded_sample.txt"
    print(f"\n=== 4. Downloading object '{object_name}' to '{local_download_file}' ===")
    client.fget_object(
        bucket_name=bucket_name,
        object_name=object_name,
        file_path=local_download_file,
    )
    print("Download completed successfully!")

    # Read downloaded file content
    with open(local_download_file, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"\nDownloaded File Content:\n{content.strip()}")

if __name__ == "__main__":
    run_upload_download_demo()
