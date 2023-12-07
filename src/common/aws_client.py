import boto3
from loguru import logger
from botocore.exceptions import ClientError


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

    def get_buckets(self) -> list:
        if self.resource == 's3':
            return self.client.list_buckets()
        else:
            logger.info('The resource it no S3 bucket')

    class S3Client:
        pass


aws = AwsClient('s3', AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_REGION)
aws.client.close()