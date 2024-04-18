from enum import Enum


class UserType(str, Enum):
    comprador = "comprador"


class UserTypePrivileged(str, Enum):
    admin = "admin"
    vendedor = "vendedor"


class CheckoutStatus(str, Enum):
    # TODO -> add checkout redirection URL for each status
    success = "success"
    failure = "failure"
    pending = "pending"


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
