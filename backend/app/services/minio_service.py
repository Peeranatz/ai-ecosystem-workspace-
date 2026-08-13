import io
from typing import Optional, List, Dict, Any
from minio import Minio
from minio.error import S3Error
from app.core.config import settings
from app.utils.logger import logger

class MinIOService:
    _client: Optional[Minio] = None

    @classmethod
    def get_client(cls) -> Minio:
        if cls._client is None:
            cls._client = Minio(
                endpoint=settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ROOT_USER,
                secret_key=settings.MINIO_ROOT_PASSWORD,
                secure=settings.MINIO_SECURE
            )
        return cls._client

    @classmethod
    def ensure_bucket_exists(cls, bucket_name: str) -> bool:
        client = cls.get_client()
        try:
            if not client.bucket_exists(bucket_name):
                client.make_bucket(bucket_name)
                logger.info(f"Created MinIO bucket: '{bucket_name}'")
            return True
        except S3Error as err:
            logger.error(f"MinIO bucket error for '{bucket_name}': {err}")
            return False

    @classmethod
    def upload_file_bytes(cls, bucket_name: str, object_name: str, data: bytes, content_type: str = "application/octet-stream") -> Dict[str, Any]:
        cls.ensure_bucket_exists(bucket_name)
        client = cls.get_client()
        data_stream = io.BytesIO(data)
        size = len(data)
        
        result = client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=data_stream,
            length=size,
            content_type=content_type
        )
        logger.info(f"MinIO upload success: {object_name} to bucket '{bucket_name}' (version_id={result.version_id})")
        return {
            "bucket_name": result.bucket_name,
            "object_name": result.object_name,
            "version_id": result.version_id,
            "etag": result.etag,
            "size_bytes": size,
            "minio_path": f"{bucket_name}/{object_name}"
        }

    @classmethod
    def download_file_bytes(cls, bucket_name: str, object_name: str, version_id: Optional[str] = None) -> Optional[bytes]:
        client = cls.get_client()
        try:
            response = client.get_object(bucket_name, object_name, version_id=version_id)
            data = response.read()
            response.close()
            response.release_conn()
            return data
        except S3Error as err:
            logger.error(f"Failed to download object {object_name} from MinIO: {err}")
            return None

    @classmethod
    def list_bucket_objects(cls, bucket_name: str, prefix: Optional[str] = None) -> List[Dict[str, Any]]:
        client = cls.get_client()
        if not client.bucket_exists(bucket_name):
            return []
        
        objects = client.list_objects(bucket_name, prefix=prefix, recursive=True)
        result = []
        for obj in objects:
            result.append({
                "object_name": obj.object_name,
                "size_bytes": obj.size,
                "last_modified": obj.last_modified.isoformat() if obj.last_modified else None,
                "version_id": obj.version_id
            })
        return result
