from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    location = 'private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False


class EmailMediaStorage(S3Boto3Storage):
    location = 'emails'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False


class EmailAttachmentMediaStorage(S3Boto3Storage):
    location = 'email-attachments'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False


class GeneratedFilesStorage(S3Boto3Storage):
    location = 'generate-files'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False


class FileTemplateMediaStorage(S3Boto3Storage):
    location = 'files-templates'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False
