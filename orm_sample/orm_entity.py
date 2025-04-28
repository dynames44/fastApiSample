from sqlalchemy import Column, String, DateTime, func, Integer, Float, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    def to_dict(self):
        
        result = {}
        
        for column in self.__table__.columns:
            value = getattr(self, column.name, None)
            
            # null 일때 기본값 
            if value is None: 
                if isinstance(column.type, String):
                    result[column.name] = ""
                    
                elif isinstance(column.type, (Integer, Float)):
                    result[column.name] = 0
                    
                else:
                    result[column.name] = None  # 나머지는 그냥 None
            else:
                result[column.name] = value

        return result

class SysUser(BaseModel):
    __tablename__ = "tb_sys_user"

    '''
        Column 옵션 
        - 데이터 타입 : String, Integer, DateTime, Boolean, Float...
        - primary_key = true/false :  PK  
        - nullable = true/false : null 허용여부
        - autoincrement = True : 자동증가 필드
        - unique = True : unique 제약 조건 사용 
        - default=... : 기본값
        - DateTime 필드의 현재시간을 넣을때는 server_default=func.now() 사용  
        - index = True : 해당 Column을 인덱스 키로 생성 
    '''
    user_id = Column(String, primary_key=True)
    user_nm = Column(String)
    user_pw = Column(String)
    use_yn = Column(String(1))
    email = Column(String(20))
    reg_dttm = Column(DateTime, server_default=func.now())
    
    '''
        수동 등록 쌉가능......
        def to_dict(self):
            return {
                "user_id": self.user_id
                ,"user_nm": self.user_nm
                ,"user_pw": self.user_pw
                ,"use_yn": self.use_yn
                ,"email": self.email
                ,"reg_dttm": self.reg_dttm            
                
            }    
    '''

class UserEtc(BaseModel):
    
    __tablename__ = "tb_user_etc"

    user_id = Column(String, primary_key=True)
    etc_info1 = Column(String(50))
    etc_info2 = Column(String(50))
    etc_info3 = Column(String(50))
    etc_info4 = Column(String(50))
    etc_info5 = Column(String(50))        
    reg_dttm = Column(DateTime, server_default=func.now())    