from pydantic import BaseModel,Field, model_validator

#data class 는 뭔가?

class pydanticBase1(BaseModel):
    name: str 
    description: str 
    price: float 
    tax: float = None
    
class pydanticBase2(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: str = Field(None, max_length=500)
    price: float = Field(..., ge=0)
    tax: float = None    
    
    