import os
import json
from minio import Minio
from io import BytesIO

class MinioLoader:
    def __init__(self):
        # Initialize MinIO client using environment variables
        self.client = Minio(
            os.getenv("MINIO_ENDPOINT", "minio:9000"),
            access_key=os.getenv("MINIO_ACCESS_KEY", "admin"),
            secret_key=os.getenv("MINIO_SECRET_KEY", "supersecretkey"),
            secure=False
        )
        self.raw_bucket = "raw-data"
        self.processed_bucket = "processed-data"

    def save_data(self, bucket_name, file_name, data):
        # Convert dictionary or list to JSON bytes, otherwise convert to string bytes
        if isinstance(data, (dict, list)):
            bytes_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        else:
            bytes_data = str(data).encode('utf-8')
            
        self.client.put_object(
            bucket_name,
            file_name,
            data=BytesIO(bytes_data),
            length=len(bytes_data)
        )
        return f"s3://{bucket_name}/{file_name}"

    def load_raw(self, file_name, data):
        # Load data into raw-data bucket
        return self.save_data(self.raw_bucket, file_name, data)

    def load_processed(self, file_name, data):
        # Load processed data into processed-data bucket
        return self.save_data(self.processed_bucket, file_name, data)