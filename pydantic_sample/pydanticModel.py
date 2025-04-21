from typing import Annotated, Optional
from pydantic import BaseModel,Field, model_validator

#데이터형, 필수 여부만 제약..
class Item(BaseModel):
    name: str
    description: str
    price: float
    tax: float | None = None
    
    #tax가  price 크면 에러 처리 : 후처리 
    @model_validator(mode='after')
    def tax_must_be_less_than_price(cls, values):
        price = values.price
        tax = values.tax
        if tax:
            if tax > price:
                raise ValueError("세금이 물건 값 보다 더쌤!!!!")

        return values 
    
#값에 따른 제약추가 
class ItemExtd(BaseModel):
    name: Annotated[str, Field(..., min_length=2)]
    description: Annotated[Optional[str], Field(None, max_length=100)]
    price: Annotated[float, Field(..., ge=0)] 
    tax: Annotated[Optional[float], Field(None, ge=0)]
    
    #tax가  price 크면 에러 처리 : 후처리 
    @model_validator(mode='after')
    def tax_must_be_less_than_price(cls, values):
        price = values.price
        tax = values.tax
        if tax:
            if tax > price:
                raise ValueError("세금이 물건 값 보다 더쌤!!!!")

        return values