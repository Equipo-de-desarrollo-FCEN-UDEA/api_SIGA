from __future__ import annotations

from boto3 import resource
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse

from app.core.config import settings


class AmazonS3:

    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.s3 = resource(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

    def push_data_to_s3_bucket(self, bucket_name, data, file_name, content_type) -> bool:
        print(settings.aws_user)
        print(settings.aws_access_key_id)
        print(settings.aws_access_secret_key)
        print(settings.aws_region_name)
        print(settings.aws_bucket_name)
        try:
            self.s3.Object(bucket_name, file_name).upload_fileobj(
                data,
                ExtraArgs={
                    'ContentType': content_type,
                },
            )
        except ClientError as e:
            raise e
        return JSONResponse(
            status_code=200,
            content={'message': 'Files uploaded'},
        )

    def delete_contents_s3_bucket(self, bucket_name, file_name) -> bool:
        try:
            self.s3.Object(bucket_name, file_name).delete()
        except ClientError as e:
            raise e
        return JSONResponse(
            status_code=200,
            content={'message': 'Files deleted'},
        )

    def get_data_from_s3_bucket(self, bucket_name, file_name):
        return self.s3.Object(bucket_name, file_name).get()

    def empty_bucket(self, bucket_name):
        self.s3.Bucket(bucket_name).objects.all().delete()


s3 = AmazonS3(
    settings.aws_access_key_id,
    settings.aws_access_secret_key, settings.aws_region_name,
)
