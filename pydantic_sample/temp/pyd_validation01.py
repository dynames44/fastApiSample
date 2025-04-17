from pydantic import BaseModel, ValidationError, ConfigDict, Field, Strict
from typing import List, Annotated

class Address(BaseModel):
    street: str
    city: str
    country: str

class User(BaseModel):
    #Strict 입력값의 자료형 자동 변환을 허용할지 여부를 설정하는 옵션입니다.
    #strict=True → 자동 형변환 허용 안 함, 타입이 정확히 일치해야 함
    #strict=False → 자동 형변환 허용, 예: "123"(문자열)도 int로 받아들임    
    # model_config = ConfigDict(strict=True) #모델 전체에 Strict 적용 

    userIdx: int                
    userNm: str                 
    useYn: str                  
    userEmail: str
    addresses: List[Address]              
    
    #개별 필드에 Strict 모드 설정 시 Field나 Annotated 이용. None 적용 시 Optional
    #loginCnt: int | None = None   
    #loginCnt: int = Field(None, strict=True)
    loginCnt: Annotated[int, Strict()] = None   

try:
    user = User(
         userIdx=1
        ,userNm="test_name"
        ,userEmail="tname@example.com"
        ,useYn="Y"
        #,addresses={"street": "123 Main St", "city": "Hometown", "country": "USA"}
        ,addresses=[{"street": "123 Main St", "city": "Hometown", "country": "USA"}]
        ,loginCnt = 4
    )
    
    print("user::::::",user)
    
except ValidationError as e:
    print("validation error")
    print(e)

