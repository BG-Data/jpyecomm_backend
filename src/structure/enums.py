# from enum import Enum

# class UserBase(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     email: str


# class UserSchema(UserBase):
#     id: int
#     name: str
#     password: str
#     birth_date: date
#     lgpd: bool
#     document: str
#     document_type: str
#     user_type: str


# class UserGetEnum(Enum):
#     name: str
#     birth_date: date
#     lgpd: bool
#     document: str
#     document_type: str
#     user_type: str