from pydantic import BaseModel, EmailStr, Field, HttpUrl, AnyUrl, AnyHttpUrl, FileUrl, IPvAnyAddress, IPvAnyNetwork, IPvAnyInterface, ValidationError

#from pydantic_extra_types.country import CountryAlpha3 국제 표준으로 사용되는 검증 형태를 미리 만들어놈 
#https://docs.pydantic.dev/latest/api/pydantic_extra_types_color/ 참조 

#pydantic이 만들어논 검증 라이브러리 ...
#굳이 pattern을 이용해 체크 안해도 되도록.....
class UserResource(BaseModel):
    email: EmailStr # 문자열 Email 검증. 
    http_url: HttpUrl #http 또는 https만 허용, host, TLD 필요 
    any_url: AnyUrl # url 형태 허용 ***://***** host 필요, TLD 필요 없음. 
    any_http_url: AnyHttpUrl #http 또는 https만 허용, host, TLD 필요 없음.  
    file_url: FileUrl   #파일 프로토콜만 허용, ftp 아님, file://*******,  host 명이 필요하지 않음. , host, TLD 필요 없음.  
    ip_address: IPvAnyAddress | None = None #CIDR 불가 (/24)
    network: IPvAnyNetwork | None = None  #CIDR 필수 (/24)
    interface: IPvAnyInterface | None = None 

try:
    user_resource = UserResource(
        email="user@examples.com",
        http_url="https://www.example.com",
        any_url="ftp://example.com",
        any_http_url="http://www.example.com",
        file_url="file://path/to/file.txt",
        ip_address="192.168.1.1",
        network="192.168.1.0/24",
        interface="192.168.1.0/24"        
    )
    
    print(user_resource)
    
except ValidationError as e:
    print(e)
