import boto3
from botocore.exceptions import ClientError

from project import EnvironmentConfig, get_logger

class StorageClient:
    _s3_client = None
    _bucket_name = None

    @classmethod
    def setup_logger(cls):
        logger = get_logger()
        return logger
    @classmethod
    def get_env_details(cls):
        logger = cls.setup_logger()
        storage_enabled = EnvironmentConfig.get_string('storage.enabled')
        if storage_enabled:
            url = EnvironmentConfig.get_string('storage.url')
            access_key = EnvironmentConfig.get_string('storage.access_key')
            secret_key = EnvironmentConfig.get_string('storage.secret_key')
            bucket_name = EnvironmentConfig.get_string('storage.bucket_name')
            if not url:
                logger.error('Storage URL not configured')
                exit(1)
            if not access_key:
                logger.error('Storage access key not configured')
                exit(1)
            if not secret_key:
                logger.error('Storage secret key not configured')
                exit(1)
            if not bucket_name:
                logger.error('Storage bucket name not configured')
                exit(1)
            return url, access_key, secret_key, bucket_name
        else:
            return None, None, None, None

    @classmethod
    async def initialize_storage_client(cls):
        if cls._s3_client is None:
            logger = cls.setup_logger()
            url, access_key, secret_key, bucket_name = cls.get_env_details()
            if url:
                try:
                    client = boto3.client(
                        service_name='s3',
                        endpoint_url=url,
                        aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key
                    )
                    client.head_bucket(Bucket=bucket_name)
                    cls._s3_client = client
                    cls._bucket_name = bucket_name
                except ClientError as client_error:
                    response = client_error.response.get('Error',{})
                    if len(response.keys()) > 0:
                        error_code = response.get('Code', 'Unknown')
                        if error_code == '404':
                            logger.error('Storage bucket not found')
                            exit(1)
                        elif error_code == '403':
                            logger.error('Storage bucket not found')
                            exit(1)
                        else:
                            logger.error('Got the following error code: {}'.format(error_code))
                            exit(1)
                    else:
                        logger.error('Unsupported error code: {}'.format(client_error))
                        exit(1)

    @classmethod
    def get_client(cls):
        if cls._s3_client is None:
            logger = cls.setup_logger()
            logger.error('Storage client not initialized')
            raise ConnectionError("S3 Client is not initialized")
        return cls._s3_client

    @classmethod
    def get_bucket_name(cls):
        if cls._s3_client is None:
            logger = cls.setup_logger()
            logger.error('Storage bucket name not initialized')
            raise ConnectionError("S3 Client is not initialized")
        return cls._bucket_name