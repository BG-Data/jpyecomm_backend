from typing import Union
import boto3
from loguru import logger
from os import path
from uuid import uuid4
from botocore.exceptions import ClientError
AWS_ACCESS_KEY='AKIAQBL4DL32K5EXWIY7'
AWS_SECRET_ACCESS_KEY='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'
AWS_REGION='us-east-1'
AWS_BUCKET_NAME='jpycomm-bucket'
AWS_BUCKET_FOLDER='product-files'
AWS_BUCKET_FOLDER_PATH='https://jpycomm-bucket.s3.amazonaws.com/product-files/'


class AwsClient:

    def __init__(self,
                 resource: str,
                 access_key: str,
                 secret_access_key: str,
                 region: str):
        self.resource = resource
        self.region = region
        self.client = boto3.client(service_name=resource,
                                   aws_access_key_id=access_key,
                                   aws_secret_access_key=secret_access_key,
                                   region_name=region)

    def get_buckets(self) -> Union[list, dict]:
        '''Get buckets

        Returns: a list of buckets and details of AWS account

        '''
        if self.resource == 's3':
            return self.client.list_buckets()
        else:
            name = 'The resource is not S3 bucket'
            logger.info(name)
            return {"status": name}

    def upload_file(self, file_name: str,
                    bucket: str,
                    object_name: str = None,
                    public_file: bool = True) -> dict:
        """Upload a file to an S3 bucket

        Args:

            - file_name: File to upload
            - bucket: Bucket to upload to
            - object_name: S3 object name. If not specified then file_name is used

        Returns: True if file was uploaded, else False
        """

        # Upload the file
        try:
            if public_file:
                response = self.client.upload_file(file_name, bucket, object_name,
                                                   ExtraArgs={'ACL': 'public-read'})
            else:
                response = self.client.upload_file(file_name, bucket, object_name)
            logger.info(response)
        except ClientError as e:
            logger.error(e)
            return {'status': False,
                    'file': file_name,
                    'url': object_name}
        return {'status': True,
                'urls': object_name}

    def delete_file(self,
                    bucket: str,
                    object_name: str,):
        try:
            response = self.client.delete_object(Bucket=bucket,
                                                 Key=object_name)
            logger.info(response)
            return {'status': response.get('DeleteMarker')}
        except ClientError as e:
            logger.error(e)
            return {'status': False,
                    'url': object_name}
