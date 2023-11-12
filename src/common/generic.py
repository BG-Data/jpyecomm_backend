from pydantic import BaseModel
from structure.connectors import Base, get_session
from sqlalchemy.orm import Session
from sqlalchemy import text, or_
from typing import Any, Union, List
from common import DatabaseSessions
from loguru import logger
import sys
from fastapi import APIRouter, HTTPException, Depends, Request, status
from datetime import date, datetime
from utils import ModelUtils

logger.add(sys.stderr, colorize=True,
           format="<yellow>{time}</yellow> {level} <green>{message}</green>",
           filter="CrudService", level="INFO")


class CrudService(DatabaseSessions):
    def __init__(self,
                 model: Base,
                 schema: BaseModel):
        self.base_schema = schema
        self.model = model
        self.model_util = ModelUtils(model)

    def get_itens(self,
                  kwargs: dict,
                  session: Session) -> List[BaseModel]:
        # TODO -> refatorar para incluir cinco esquemas em um padrão de contrato front/back bem definido para: filtros, ordernação, agrupamento, limit/offset/paginação e joins
        'Recupera itens de acordo com os argumentos adicionados em dicionário'
        try:
            item = session.query(self.model)
            if (limit := kwargs.pop('limit', 10)):
                logger.info(f"limite aplicado {limit}")
                limit = int(limit)
            if (offset := kwargs.pop('offset', 0)):
                logger.info(f"offset aplicado {offset}")
            self.model_util.check_model_kwargs(kwargs)
            kwargs = self.model_util.convert_model_attributes(kwargs)
            if kwargs:
                sql_order_by_list, kwargs = self.model_util.order_by_conditions(kwargs)
                sql_filters = self.model_util.filter_conditions(kwargs)
                item = item.filter(text(sql_filters.get('filter'))).params(sql_filters.get('values'))
            item = item.limit(limit).offset(offset).order_by(*sql_order_by_list)
            return [self.base_schema.model_validate(queried) for queried in item.all()]
        except Exception as exp:
            logger.error(f'Erro at >>>>> get_itens: {exp}')
            raise exp

    def insert_item(self,
                    insert_schema: BaseModel,
                    session: Session) -> BaseModel:
        try:
            item = self.model(**insert_schema.model_dump(exclude={'id'}))
            item = self.create_session(session, item)
            return self.base_schema.model_validate(item)
        except Exception as exp:
            logger.error(f'Erro at >>>>> insert_itens: {exp}')
            raise exp
        
    def update_item(self,
                    item_id: int,
                    update_schema: BaseModel,
                    session: Session):
        try:
            if hasattr(self.model, 'email'):
                item = session.query(self.model).filter(or_(self.model.id == item_id,
                                                            self.model.email == update_schema.email))
            else:
                item = session.query(self.model).filter(self.model.id == item_id)
            if not item:
                logger.error('No item was found to be updated')
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail={'status': status.HTTP_400_BAD_REQUEST,
                                            'info': f'No user found with this id: {id}'})
            to_update = update_schema.model_dump(exclude_unset=True,
                                                 exclude_none=True)
            upd_result = item.update(to_update)
            self.update_session(session, item)
            logger.info(f"Rows updated: {upd_result}")
            logger.info(f'{update_schema.__repr_name__()} with id: {item.one().id} changed to {to_update}')
            upd_result = session.query(self.model).filter(self.model.id == item_id)
            return self.base_schema.model_validate(upd_result.one())
        except Exception as exp:
            logger.error(f'Erro no >>>>> insert_itens: {exp}')
            raise exp
        
    def delete_item(self,
                    item_id: int,
                    session: Session):
        try:
            item = session.query(self.model).filter(self.model.id == item_id).one()
            if not item:
                logger.error('No item was found to be deleted')
                raise ValueError('Delete item not found')
            # del_result = item.delete()
            self.delete_session(session, item)
            logger.info('Row deleted')
            logger.info(f'{item.__tablename__} tabled deleted row with id {item_id}')
            return {'status': 'deleted',
                    "table":
                        {"name": item.__tablename__,
                         'id': item.id}
                    }
        except Exception as exp:
            logger.error(f'Error at >>>>> [Function name]: {exp}')
            raise exp


class CrudApi(APIRouter):

    def __init__(self,
                 model: Base,
                 schema: BaseModel,
                 insert_schema: BaseModel,
                 update_schema: BaseModel,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.insert_schema = insert_schema
        self.update_schema = update_schema
        self.crud = CrudService(model, schema)

    def get(self,
            id: int = None,
            limit: int = 5,
            offset: int = 0,
            get_schema: Request = None,
            session: Session = Depends(get_session)):
        try:
            params = get_schema.query_params._dict
            return self.crud.get_itens(params, session)
        except Exception as exp:
            logger.error(f'Error at >>>>> get_item {exp}')
            raise HTTPException(status_code=400, detail=str(exp))

    def insert(self,
               insert_schema: BaseModel,
               session: Session = Depends(get_session)):
        try:
            insert_schema = self.insert_schema if not insert_schema else insert_schema
            return self.crud.insert_item(insert_schema, session)
        except Exception as exp:
            logger.error(f'Error at >>>>> insert_item {exp}')
            raise HTTPException(status_code=400, detail=str(exp))

    def update(self,
               item_id: int,
               update_schema: BaseModel,
               session: Session = Depends(get_session)):
        try:
            update_schema = self.update_schema if not update_schema else update_schema
            return self.crud.update_item(item_id, update_schema, session)
        except Exception as exp:
            logger.error(f'Error at >>>>> update_item {exp}')
            raise HTTPException(status_code=400, detail=str(exp))
    
    def delete(self,
               item_id: int,
               session: Session = Depends(get_session)):
        try:
            return self.crud.delete_item(item_id, session)
        except Exception as exp:
            logger.error(f'Error at >>>>> delete_item {exp}')
            raise HTTPException(status_code=400, detail=str(exp))
