from pydantic import BaseModel
from structure.connectors import Base
from sqlalchemy.orm import Session
from typing import Any, Union


class CrudService:
    def __init__(self,
                 model: Base,
                 schema: BaseModel):
        self.schema = schema
        self.model = model
    
    def __check_model(self):
        pass

    def get_itens(self,
                  kwargs: dict,
                  model: Union[Base, Any],
                  session: Session):
        query = session.query(model)
        if kwargs.get('limit'):
            query = query.limit(kwargs.pop('limit'))
        if kwargs:
            query = query.filter_by(**kwargs)
        return [self.schema.model_validate(queried) for queried in query.all()]
