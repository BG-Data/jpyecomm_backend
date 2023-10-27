from pydantic import BaseModel
from structure.connectors import Base, get_session
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Any, Union, List
from common.general_classes import database_sessions
from loguru import logger
import sys
from fastapi import APIRouter, HTTPException, Depends, Request
from datetime import date

logger.add(sys.stderr, colorize=True,
           format="<yellow>{time}</yellow> {level} <green>{message}</green>",
           filter="CrudService", level="INFO")


class CrudService(database_sessions):
    def __init__(self,
                 model: Base,
                 schema: BaseModel):
        self.base_schema = schema
        self.model = model

    def __check_model(self):
        'Adicionar um kwarg checker para criar exceção do tipo Valor'
        pass

    def __filter_conditions(self, kwargs: dict) -> dict:
        'Generic filtering conditions. >>>.No operators for now'
        filter_conditions = []
        values = {}
        i = 0  # gambeta
        for k, v in kwargs.items():
            param_key = f"value_{i}"
            values[param_key] = v
            if isinstance(v, (int, float, bool)):
                filter_conditions.append(f"{k} = :{param_key}")
            elif isinstance(v, str):
                filter_conditions.append(f"{k} LIKE :{param_key}")
            elif isinstance(v, date):
                filter_conditions.append(f"{k} BETWEEN :{param_key} AND {date.today()}")
            i += 1
        if i == 1:
            return {"filter": ' '.join(filter_conditions),
                    "values": values}
        return {"filter": ' AND '.join(filter_conditions),
                "values": values}
    
    def get_itens(self,
                  kwargs: dict,
                  session: Session) -> List[BaseModel]:
        'Recupera itens de acordo com os argumentos adicionados em dicionário'
        try:
            item = session.query(self.model)
            if (limit := kwargs.pop('limit', None)):
                # add pagination in the near future
                item = item.limit(limit)
            if kwargs:
                sql_filters = self.__filter_conditions(kwargs)
                item = item.filter(text(sql_filters.get('filter'))).params(sql_filters.get('values'))
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
            item = session.query(self.model).filter(self.model.id == item_id)
            if not item:
                logger.error('No item was found to be updated')
                raise ValueError('Update item not found')
            upd_result = item.update(update_schema.model_dump(exclude_unset=True))
            logger.info(f"Rows updated: {upd_result}")
            self.update_session(session, item)
            upd_result = session.query(self.model).filter(self.model.id == item_id)
            return self.base_schema.model_validate(upd_result.one())
        except Exception as exp:
            logger.error(f'Erro no >>>>> insert_itens: {exp}')
            raise exp
        
    def delete_item(self,
                    item_id: int,
                    session: Session):
        try:
            item = session.query(self.model).filter(self.model.id == item_id)
            if not item:
                logger.error('No item was found to be updated')
                raise ValueError('Update item not found')
            del_result = item.delete()
            logger.info(f'Rows deleted: {del_result}')

            item = session.query(self.model).filter(self.model.id == item_id)
            return 
        except Exception as exp:
            logger.error(f'Error at >>>>> [Function name]: {exp}')
            raise exp

    def __template_itens(self,
                        item_id: int,
                        schema: BaseModel,
                        session: Session):
        try:
            pass
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
            limit: int = None,
            get_schema: Request = None,
            session: Session = Depends(get_session)):
        try:
            params = get_schema.query_params._dict
            if id:
                params.update({'id': int(id)})
            else:
                params.update({'limit': int(limit)})
            return self.crud.get_itens(params, session)
        except Exception as exp:
            logger.error(f'Error at >>>>> get_item {exp}')
            raise exp

    def insert(self,
               insert_schema: BaseModel,
               session: Session = Depends(get_session)):
        try:
            insert_schema = self.insert_schema if not insert_schema else insert_schema
            return self.crud.insert_item(insert_schema, session)
        except Exception as exp:
            logger.error(f'Error at >>>>> insert_item {exp}')
            raise exp

    def update(self,
               item_id: int,
               update_schema: BaseModel,
               session: Session = Depends(get_session)):
        try:
            update_schema = self.update_schema if not update_schema else update_schema
            return self.crud.update_item(item_id, update_schema, session)
        except Exception as exp:
            logger.error(f'Error at >>>>> update_item {exp}')
            raise exp
    
    def delete(self,
               item_id: int,
               session: Session = Depends(get_session)):
        try:
            return self.crud.delete_item(item_id, session)
        except Exception as exp:
            logger.error(f'Error at >>>>> delete_item {exp}')
            raise exp
