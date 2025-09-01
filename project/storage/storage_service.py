from fastapi import UploadFile
import io

from common.exceptions.config_exceptions import StorageException
from project import EnvironmentConfig, get_logger
from project.storage.client import StorageClient

class StorageService:
    def __init__(self):
        self.s3_client = StorageClient.get_client()
        self.bucket = StorageClient.get_bucket_name()
        self.key_prefix = EnvironmentConfig.get_string('storage.default_key')
        self.logger = get_logger()

    async def upload_file(self, file:UploadFile, key:str):
        new_key = f'{self.key_prefix}_{key}'
        self.s3_client.upload_fileobj(file.file,self.bucket,new_key)
        return True

    async def download_file(self, key:str):
        new_key = f'{self.key_prefix}_{key}'
        try:
            file_stream = io.BytesIO()
            self.s3_client.download_fileobj(self.bucket, new_key, file_stream)
            file_stream.seek(0)
            return file_stream
        except Exception as e:
            self.logger.error(e)
            raise StorageException(e)

