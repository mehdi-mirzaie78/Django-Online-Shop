import boto3
from botocore.exceptions import ClientError
from django.conf import settings
import os


class Bucket:
    """
    CDN Bucket manager

    init method creates a connection to arvan cloud.
    """

    def __init__(self):
        session = boto3.session.Session()
        self.conn = session.client(
            service_name=settings.AWS_SERVICE_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL
        )

    def get_objects(self):
        result = self.conn.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        if result['KeyCount']:
            return result['Contents']
        return None

    def delete_object(self, key):
        self.conn.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)
        return True

    def download_object(self, key):
        self.conn.download_file(settings.AWS_STORAGE_BUCKET_NAME, key, settings.AWS_LOCAL_STORAGE + key)
        return True

        # with open(settings.AWS_LOCAL_STORAGE + key, 'wb') as f:
        #     self.conn.download_fileobj(settings.AWS_STORAGE_BUCKET_NAME, key, f)
        # return True

    def upload_object(self, key):
        self.conn.upload_file(settings.AWS_LOCAL_STORAGE + key, settings.AWS_STORAGE_BUCKET_NAME, key)
        return True

        # with open(settings.AWS_LOCAL_STORAGE + key, 'rb') as f:
        #     self.conn.upload_fileobj(f, settings.AWS_STORAGE_BUCKET_NAME, key)
        # return True


bucket = Bucket()
