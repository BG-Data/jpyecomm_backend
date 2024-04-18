from pydantic import BaseModel, Field


class Aliases(BaseModel):
    # TODO -> Add checkout response db insertion procedures (failure, under way, complete, finished , whatever there is)
    CHECKOUT_RESPONSE: dict = Field(
        description="Checkout response model, returns the failure or success of a checkout process.",
        default={"status": str(), "detail": str()},
    )
