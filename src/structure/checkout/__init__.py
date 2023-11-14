from structure.schemas import PydanticModel
from typing import List


# TODO -> Finish Pydantic models for checkout procedures

class CheckoutPayerPhone(PydanticModel):
        area_code: str
        number: 

class CheckoutPayer(PydanticModel):
        name: str
        surname: str
        email: str
        phone: CheckoutPayerPhone

class CheckoutPayload(PydanticModel):
    

    items = List[CheckoutItems]
    payer: CheckoutPayer
    identification: CheckoutId
    address: CheckoutAddr


