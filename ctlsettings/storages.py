from storages.backends.s3 import S3Storage, S3StaticStorage


class UploadsStorage(S3Storage):
    location = 'uploads'


class MediaStorage(S3StaticStorage):
    location = 'media'
