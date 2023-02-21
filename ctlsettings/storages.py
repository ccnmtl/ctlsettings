from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage


class UploadsStorage(S3Boto3Storage):
    location = 'uploads'


class MediaStorage(S3StaticStorage):
    location = 'media'
