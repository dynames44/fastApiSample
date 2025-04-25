from typing import Annotated, Optional
from pydantic import BaseModel,Field

# 공통으로 사용가능한 Model 생성
class BaseUserId(BaseModel):
    user_id: Annotated[str, Field(...)]

class sys_user(BaseUserId): # 공통모델 상속받고 추가 항목만....
    user_nm: Annotated[str, Field(None, max_length=50)]
    user_pw: Annotated[Optional[str], Field(None, min_length=2, max_length=20)]
    use_yn: Annotated[Optional[str], Field(None, max_length=1)]
    email: Annotated[Optional[str], Field(None, max_length=100)]
    
class user_etc(BaseUserId): # 공통모델 상속받고 추가 항목만....
    etc_info1: Annotated[Optional[str], Field(None, max_length=50)]    
    etc_info2: Annotated[Optional[str], Field(None, max_length=50)]        
    etc_info3: Annotated[Optional[str], Field(None, max_length=50)]        
    etc_info4: Annotated[Optional[str], Field(None, max_length=50)]        
    etc_info5: Annotated[Optional[str], Field(None, max_length=50)]        

class find_user(BaseUserId):
    pass
    
class serch_model(BaseModel):
    use_yn: Annotated[Optional[str], Field(None, max_length=1)]
    email: Annotated[Optional[str], Field(None, max_length=20)]
