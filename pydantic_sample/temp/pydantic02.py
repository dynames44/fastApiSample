from pydantic import BaseModel

#Pydantic 모델 정의
class User(BaseModel):
    userIdx: int       
    userNm: str        
    userEmail: str     

# User를 상속받아 'useYn' 필드를 추가한 확장 모델
class UserExtends(User):
    useYn: str

#UserExtends를 상속받아 'userTp' 필드를 추가한 최종 모델
class LastUser(UserExtends):
    userTp: str | None = None  # 사용자 타입 (선택 입력)

#User 인스턴스 생성 
user = User(
    userIdx=1,
    userNm="userNm",
    userEmail="userNm@example.com"
)

#UserExtends 인스턴스 생성
userExtends = UserExtends(
    userIdx=2,
    userNm="userNm2",
    userEmail="userNm2@example.com",
    useYn="N"
)

#LastUser 인스턴스 생성
lastUser = LastUser(
    userIdx=3,
    userNm="userNm3",
    userEmail="userNm3@example.com",
    useYn="Y",
    userTp="M"
)

#  Pydantic 모델 인스턴스를 딕셔너리 형태로 변환함 : 얕은 복사
test1 = user.model_dump()
test1["useYn"] = "Y"
test1["userTp"] = "M"

print("user :::::", type(user), user)
print("userExtends:::::", type(userExtends), userExtends)
print("lastUser:::::", type(lastUser), lastUser)
print("test1:::::", type(test1), test1)
print()

#dict 데이터를 **언패킹(unpacking)** 해서 Pydantic 모델로 다시 생성
expLastUser = LastUser(**test1)
print("expLastUser:::::", type(expLastUser), expLastUser)
print()

#Pydantic 모델을 다양한 형태로 복사 또는 직렬화할 수 있다.
# model instance → dict 로 변환 (직렬화)
dump1 = user.model_dump()
print("dump1::::::", type(dump1), dump1)

# model instance → JSON 문자열로 변환 (JSON 직렬화)
dump2 = user.model_dump_json()
print("dump2:::::::", type(dump2), dump2)

# model instance → 동일한 Pydantic 인스턴스로 복사  (deep copy)
dump3 = user.model_copy()
print("dump3::::::", type(dump3), dump3)
print()