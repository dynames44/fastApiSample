import json
from pydantic import BaseModel

#계층 구조의 Pydantic 모델 정의 Case
# 하위 구조를 가진 Address 모델 정의
class Address(BaseModel):
    street: str    # 거리명
    city: str      # 도시명

# Address 모델을 포함하는 상위(User) 모델 정의
# - 계층 구조(Nested 구조)의 모델 클래스 구성 예시
class UserNested(BaseModel):
    userIdx: int           # 사용자 고유 번호
    userNm: str            # 사용자 이름
    userEmail: str         # 사용자 이메일
    address: Address       # 중첩된 주소 정보 (Address 객체)

# JSON 문자열을 파싱하여 딕셔너리로 변환
json_dict = '{"userIdx": "1", "userNm": "userNm1", "userEmail": "userEmail@exp.co.ke", "address": {"street": "123 Main St", "city": "Anytown"}}'
json_dict = json.loads(json_dict)

print("json_dict:::", type(json_dict), json_dict)  # 딕셔너리로 잘 파싱되었는지 확인
print("address[city]:::", json_dict.get("address").get("city"))     # dict 접근 방식
print("address[street]:::", json_dict.get("address").get("street"))
print("---------------------------")

# dict 언패킹하여 Pydantic 모델 인스턴스 생성
# - Pydantic이 내부적으로 중첩된 구조(address)를 Address 모델로 자동 매핑함
userNested1 = UserNested(**json_dict)

print("userNested1:::", type(userNested1), userNested1)
print("address[city]:::", userNested1.address.city)    # 객체처럼 바로 접근 가능
print("address[street]:::", userNested1.address.street)
print("---------------------------")

# address를 dict로 직접 전달하여 생성
# - Pydantic은 dict 형태로 들어온 중첩 필드도 자동으로 Address 객체로 변환함
userNested2 = UserNested(
    userIdx=2,
    userNm="userNm2",
    userEmail="userEmail2@exp.co.ke",
    address={"street": "123 Main St", "city": "Anytown"}
)

print("userNested2:::", type(userNested2), userNested2)
print("address[city]:::", userNested2.address.city)
print("address[street]:::", userNested2.address.street)
print("---------------------------")

# address를 직접 Address 인스턴스로 전달
# - 이 방식은 가장 명시적이며 타입 안정성이 좋음
userNested3 = UserNested(
    userIdx=3,
    userNm="userNm3",
    userEmail="userEmail3@exp.co.ke",
    address=Address(
        street="1234",
        city="Anytown"
    )
)

print("userNested3:::", type(userNested3), userNested3)
print("address[city]:::", userNested3.address.city)
print("address[street]:::", userNested3.address.street)
