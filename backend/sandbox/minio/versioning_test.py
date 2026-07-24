import os
from minio import Minio
from minio.commonconfig import ENABLED
from minio.versioningconfig import VersioningConfig
from core.config import settings

def run_versioning_demo():
    print("=== 1. Connecting to MinIO Client ===")
    client = Minio(
        endpoint=settings.minio_endpoint,
        access_key=settings.minio_root_user,
        secret_key=settings.minio_root_password,
        secure=False
    )

    bucket_name = settings.minio_bucket
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    print(f"\n=== 2. Enabling Object Versioning on Bucket '{bucket_name}' ===")
    client.set_bucket_versioning(bucket_name, VersioningConfig(ENABLED))
    version_status = client.get_bucket_versioning(bucket_name)
    print(f"Bucket '{bucket_name}' Versioning Status: {version_status.status}")

    object_name = "my_profile_photo.txt"
    v1_file_path = "sandbox/minio/profile_v1.txt"
    v2_file_path = "sandbox/minio/profile_v2.txt"

    # Create content for Version 1
    with open(v1_file_path, "w", encoding="utf-8") as f:
        f.write("Profile Version 1: Initial Sky Profile Photo Data [Version 1.0]\n")

    # Create content for Version 2
    with open(v2_file_path, "w", encoding="utf-8") as f:
        f.write("Profile Version 2: Updated Sky Profile Photo Data [Version 2.0]\n")

    print(f"\n=== 3. Uploading Version 1 of '{object_name}' ===")
    result_v1 = client.fput_object(bucket_name, object_name, v1_file_path)
    version_id_1 = result_v1.version_id
    print(f"Uploaded Version 1 successfully! Version ID: {version_id_1}")

    print(f"\n=== 4. Uploading Version 2 (Overwriting same object name '{object_name}') ===")
    result_v2 = client.fput_object(bucket_name, object_name, v2_file_path)
    version_id_2 = result_v2.version_id
    print(f"Uploaded Version 2 successfully! Version ID: {version_id_2}")

    print("\n" + "="*50)
    print("=== TEST CASE 1: Fetching WITHOUT specifying version_id ===")
    print("="*50)
    download_path_latest = "sandbox/minio/downloaded_latest.txt"
    client.fget_object(bucket_name, object_name, download_path_latest)
    with open(download_path_latest, "r", encoding="utf-8") as f:
        latest_content = f.read()
    print(f"Result (Without version_id): {latest_content.strip()}")
    print("--> Explanation: When version_id is NOT specified, MinIO automatically returns the Latest Version (Version 2.0).")

    print("\n" + "="*50)
    print("=== TEST CASE 2: Fetching SPECIFYING version_id (Version 1 ID) ===")
    print("="*50)
    download_path_v1 = "sandbox/minio/downloaded_v1.txt"
    client.fget_object(bucket_name, object_name, download_path_v1, version_id=version_id_1)
    with open(download_path_v1, "r", encoding="utf-8") as f:
        v1_content = f.read()
    print(f"Result (With version_id={version_id_1}): {v1_content.strip()}")
    print(f"--> Explanation: When version_id='{version_id_1}' IS specified, MinIO retrieves the exact historical Version 1.0.")

if __name__ == "__main__":
    run_versioning_demo()
