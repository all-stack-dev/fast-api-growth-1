from project.storage.storage_service import StorageService
from project.cache_db.cache_service import CacheService

def get_storage_service():
    return StorageService()

def get_cache_service():
    return CacheService()
