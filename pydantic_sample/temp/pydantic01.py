import json
from pydantic import BaseModel

#Pydantic Model 기본 형태 정의
class User(BaseModel):
    userIdx: int                # 사용자 고유 번호
    userNm: str                 # 사용자 이름
    useYn: str                  # 사용 여부 (Y/N)
    userEmail: str              # 이메일 주소
    userTp: str | None = None   # 사용자 타입 (선택 입력)

#직접 Pydantic 모델 인스턴스 생성
sysUser = User(
    userIdx=1,
    userNm="test_name",
    userEmail="tname@example.com",
    useYn="N"
)

print("sysUser:::::", type(sysUser), sysUser)

# dict 데이터를 언패킹(**)하여 Pydantic 모델로 변환
# - 일반 딕셔너리를 키워드 인자로 분해해서 모델 생성
userDict = dict(
    userIdx=2,
    userNm="userNm2",
    userEmail="userNm2@example.com",
    useYn="N",
    userTp="M"
)

print("userDict:::::", type(userDict), userDict)

# 딕셔너리 언패킹 → User 모델 생성
dtUser = User(**userDict)
print("dtUser:::::", type(dtUser), dtUser)

# JSON 문자열 → 딕셔너리로 변환 → Pydantic 모델로 변환
userStr = '{"userIdx": 3, "userNm": "userNm3", "userEmail": "userNm3@example.com", "useYn": "Y", "userTp": "M"}'
print("userStr:::::", type(userStr), userStr)

#[1단계] JSON 문자열 → 딕셔너리로 변환 (json.loads 사용)
userDict = json.loads(userStr)
print("userDict:::::", type(userDict), userDict)

#[2단계] 딕셔너리 → Pydantic 모델로 변환
userDant = User(**userDict)
print("userDant:::::", type(userDant), userDant)