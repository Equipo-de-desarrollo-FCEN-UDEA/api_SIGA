from __future__ import annotations

from boto3 import client
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

        self.s3_client = client(
            's3', region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def push_data_to_s3_bucket(
            self,
            bucket_name,
            data, file_name,
            content_type,
    ) -> JSONResponse:
        try:
            self.s3.Object(bucket_name, file_name).upload_fileobj(
                data,
                ExtraArgs={
                    'ContentType': content_type,
                },
            )
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            return JSONResponse(
                status_code=400,
                content={'error': f'S3 error: {error_code} - {error_message}'},
            )
        return JSONResponse(
            status_code=200,
            content={'message': 'Files uploaded'},
        )

    def delete_contents_s3_bucket(self, bucket_name, file_name) -> JSONResponse:
        try:
            self.s3.Object(bucket_name, file_name).delete()
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            return JSONResponse(
                status_code=400,
                content={'error': f'S3 error: {error_code} - {error_message}'},
            )
        return JSONResponse(
            status_code=200,
            content={'message': 'Files deleted'},
        )

    def get_data_from_s3_bucket(self, bucket_name, file_name):
        return self.s3.Object(bucket_name, file_name).get()

    def empty_bucket(self, bucket_name):
        self.s3.Bucket(bucket_name).objects.all().delete()

    def list_documents(self, bucket_name, user_id, user_application_id):
        folder = f'{user_id}/{user_application_id}/'
        bucket = self.s3.Bucket(bucket_name)

        archivos = []
        for obj in bucket.objects.filter(Prefix=folder):
            key = obj.key
            if key.endswith('/'):
                continue  # omitir "carpetas vacías"

            signed_url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': key},
                ExpiresIn=3600,
            )
            archivos.append({
                'name': key.replace(folder, ''),  # nombre limpio
                'url': signed_url,
            })

        return archivos


s3 = AmazonS3(
    settings.aws_access_key_id,
    settings.aws_access_secret_key, settings.aws_region_name,
)
