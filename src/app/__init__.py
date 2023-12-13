from pydantic import BaseModel
from loguru import logger
from typing import List
import sys
from common import DatabaseSessions, get_current_method_name
from fastapi import HTTPException, Depends, UploadFile
from structure.connectors import Base
from sqlalchemy import or_, delete
from time import sleep
from structure.models import ProductFilesModel
from structure.schemas import ProductFileUrls
from structure.connectors import Session, get_session
from settings import cfg
from common.aws import AwsClient

logger.add(sys.stderr, colorize=True,
           format="<yellow>{time}</yellow> {level} <green>{message}</green>",
           filter="Services", level="INFO")


class UserService:
    def __init__(self,
                 model: Base,
                 schema: BaseModel):
        self.model = model
        self.base_schema = schema


class ProductService(DatabaseSessions):
    def __init__(self,
                 model: Base,
                 schema: BaseModel):
        self.model = model
        self.base_schema = schema
        self.aws_service: AwsClient = AwsClient('s3',
                                                cfg.AWS_ACCESS_KEY,
                                                cfg.AWS_SECRET_ACCESS_KEY,
                                                cfg.AWS_REGION)

    def get_product_urls(self, product_id: int,
                         session: Session = Depends(get_session)) -> List[ProductFileUrls]:
        try:
            results = session.query(ProductFilesModel)\
                            .filter(ProductFilesModel.product_id == product_id)
            return [result.file for result in results.all()]
        except Exception as exp:
            logger.error(f'Error at >>>>> get_product urls {exp}')
            raise HTTPException(status_code=500, detail=str(exp))

    def delete_product_urls(self, product_id: int = None,
                            session: Session = Depends(get_session)):
        try:
            file_data = session.query(ProductFilesModel).filter(ProductFilesModel.product_id == product_id).all()
            deleted_files_bucket = [self.aws_service.delete_file(cfg.AWS_BUCKET_NAME, file.file) for file in file_data]
            delete_statement = delete(ProductFilesModel).where(ProductFilesModel.product_id == product_id)
            result = session.execute(delete_statement)
            delete_count = result.rowcount
            if delete_count == 0:
                logger.error('No item was found to be deleted')
                return {'status': 'No urls to delete',
                        "table":
                            {"name": ProductFilesModel.__tablename__}
                        }
            logger.info(f'{delete_count} Row deleted')
            logger.info(f'{ProductFilesModel.__tablename__} tabled deleted row with id {product_id}')
            return {'status': 'deleted',
                    "table":
                        {"name": ProductFilesModel.__tablename__,
                         'product_id': product_id},
                    "bucket":
                        {"name": cfg.AWS_BUCKET_NAME,
                         "urls": deleted_files_bucket}
                    }

        except Exception as exp:
            logger.error(f'Error at >>>>> {get_current_method_name()}: {exp}')
            raise HTTPException(status_code=500, detail=str(exp))


class ProductFileService:
    def __init__(self,
                 model: Base,
                 schema: BaseModel):
        self.model = model
        self.base_schema = schema
        self.aws_service: AwsClient = AwsClient('s3',
                                                cfg.AWS_ACCESS_KEY,
                                                cfg.AWS_SECRET_ACCESS_KEY,
                                                cfg.AWS_REGION)

    async def create_product_image_url(self,
                                       insertion: UploadFile,
                                       filename: str,
                                       product_id: int) -> dict:
        content = insertion.file.read()
        with open(filename, 'wb') as f:
            f.write(content)
        result = self.aws_service.upload_file(filename,
                                              cfg.AWS_BUCKET_NAME,
                                              cfg.AWS_BUCKET_FOLDER + "/" + str(product_id) + "/" + filename)
        if result.get('status') is False:
            for j in range(3):
                sleep((j+1)**2)
                result = await self.create_product_image_url(insertion, filename, product_id)
                if result.get('status') is True:
                    break
            else:
                raise HTTPException(status_code=400, detail=f'Failed to create image URL: {result}')
        else:
            return result

    def delete_product_url(self, id: int = None,
                           session: Session = Depends(get_session)):
        try:
            file_data = session.query(ProductFilesModel).filter(ProductFilesModel.id == id).first()
            result = self.aws_service.delete_file(cfg.AWS_BUCKET_NAME, file_data.file)
            if not result.get('status'):
                logger.error('No item was found to be deleted')
                return {'status': 'not deleted',
                        "bucket":
                            {"name": cfg.AWS_BUCKET_NAME,
                             "url": file_data.file}
                        }
            logger.info(f'{result} file deleted from bucket')
            return {'status': 'deleted',
                    "bucket":
                        {"name": cfg.AWS_BUCKET_NAME,
                            "url": file_data.file}
                    }
        except Exception as exp:
            logger.error(f'Error at >>>>> {get_current_method_name()}: {exp}')
            raise HTTPException(status_code=500, detail=str(exp))


class PaymentService:
    def __init__(self,
                 model: Base,
                 schema: BaseModel):
        self.model = model
        self.base_schema = schema


class SaleService:
    def __init__(self,
                 model: Base,
                 schema: BaseModel):
        self.model = model
        self.base_schema = schema


class AddressService:
    def __init__(self,
                 model: Base,
                 schema: BaseModel):
        self.model = model
        self.base_schema = schema
