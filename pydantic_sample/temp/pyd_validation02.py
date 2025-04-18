from pydantic import BaseModel, Field, ValidationError
from typing import Optional,Annotated
from decimal import Decimal

class User(BaseModel):
    
    '''
        Field를 이용한 Validation
        - 필수, 옵션 여부 : 필수(....) / 옵션(None)
        - 기본값 : default  = "****"
        - 문자열 길이 : min_length=2, max_length=50
        - 값 제한 : gt-초과, ge-이상, lt-미만, le-이하
        - 배수 : multiple_of - 헤당 값의 배수만 허용  Ex) multiple_of=10
        - 소수점 전체 길이 - max_digits 단.데이터 형이 Decimal일때만 적용된다. Ex)max_digits=5
        - 소수점 자리수 길이 - decimal_places 단.데이터 형이 Decimal일때만 적용된다. Ex)decimal_places=2
        - 비정상 수치 허용 : allow_inf_nan - Nan등 비정상 수치 허용 여부, True- 허용, False - 허용안함 
        - 정규식 패턴 체크 :  pattern Ex) pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$"
        - 키이름 변경 : alias Ex) alias="product_name" - alias, 필드명 병행 사용원하면 model_config 이용 
        - 필드 이름 : title (문서화용 Swagger 등에 사용됨)
        - 필드 설명 : description (문서화용 Swagger 등에 사용됨)	
        - 필드 사용 중단 알림 : eprecated (문서화용 Swagger 등에 사용됨)
        - 예시 값 : example	(문서화용 Swagger 등에 사용됨)
    '''
    
    username: str = Field(...)
    email: str = Field(...,pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    password: str = Field(..., min_length=8)
    #age: Optional[int] = Field(None, ge=0, le=120)
    #age: Annotated[int, Field(None, ge=0, le=120)]
    age: int =  Field(None, ge=0, le=30)
    desc: str =  Field(None, alias="model_desc")
    is_active: bool = Field(default=True)
    mage: int =  Field(None, multiple=3)
    tdecimal : Decimal = Field(None, max_digits=5, decimal_places=2)

# Example usage
try:
    user = User(username="john_doe", email="john.doe@example.com", password="123456789")
    #user = User(username="john_doe", email="john.doe@example.com", password="1234") # password 길이 오류 
    #user = User(username="john_doe", email="john.doeexample.com", password="123456789") #email 페턴 오류 

    #Alias Test 
    userAlias = User(username="john_doe", email="john.doe@example.com", password="123456789", desc="desc test") # alias에 맞지 않아 None으로 찍힌다.
    userAlias2 = User(username="john_doe", email="john.doe@example.com", password="123456789", model_desc="desc test", age=29) #
    
    print("user::::",user)
    print("userAlias::::",userAlias)
    print("userAlias2::::",userAlias2)
    
except ValidationError as e:
    print(e.json())