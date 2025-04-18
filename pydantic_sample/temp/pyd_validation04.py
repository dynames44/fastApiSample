from pydantic import BaseModel,  ValidationError, field_validator, model_validator
from typing import Optional

class User(BaseModel):
    username: str
    password: str
    confirm_password: str
    
    #Validation Cutom
    #@field_validator("필드") : 지정된 필드에 검증 처리
    #@model_validator(처리모드) : 모델 전체 검증 처리  
     # - mode='before ' , mode='after'
     #model_validator(mode='before') → field_validator(***) → model_validator(mode='after') 순으로 검증된다.
    
    @field_validator('username')
    def username_must_not_be_empty(cls, value: str):
        
        if not value.strip():
            raise ValueError("Username must not be empty")
        
        return value

    @field_validator('password')
    def password_must_be_strong(cls, value: str):
        
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        return value
    
    @model_validator(mode='after')
    def check_passwords_match(cls, values):

        password = values.password
        confirm_password = values.confirm_password

        if password != confirm_password:
            raise ValueError("Password do not match")

        return values
    
# 검증 테스트    
try:
    user = User(username="john_doe", password="Secret123", confirm_password="Secret12")
    print(user)
except ValidationError as e:
    print(e)