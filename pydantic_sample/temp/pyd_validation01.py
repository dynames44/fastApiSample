from pydantic import BaseModel, ValidationError, Field, Strict
from typing import List, Annotated

class Address(BaseModel):
    street: str
    city: str
    country: str

class User(BaseModel):
    
    # model_config : class Model 전체에 적용될 옵션 지정 
    model_config = {
        "title": "회원정보 모델",                  # 모델 제목  (문서화용)
        "description": "회원정보 구조",         # 모델 대한 설명 (문서화용)
        "populate_by_name": True,              # 필드명, 필드 Alias 병행 사용여부 - True : 병행 가능, False: 필드 Alias만 인정 
        "strict": True,                        # 타입 자동 변환 비허용 (정확한 타입만 허용)
        "extra": "ignore"                      # 선언되지 않은 필드가 들어오면.....forbid-에러발생, ignore - 필드 무시 (모델 저장되지 않음), allow - 필드 모델 포함 (dict로 저장됨)
    }    

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

