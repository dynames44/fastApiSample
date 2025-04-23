# fastApiSample

## ✅ 파이썬 개발 가상환경 설정 가이드



### 0. 파이썬 설치, Path 설정

> 설마 파이썬 설치 안하고 저대로 했더니 안된다고 할까봐 일단 써 놓는다.



### 1. 가상환경 생성
> 외부 라이브러리를 OS 전역에 설치하지 않고 해당 프로젝트 전용으로 격리된 환경 구성

```
python -m venv venv
```



### 2. 가상환경 활성화



#### 🔹 Windows (cmd)

```
.\venv\Scripts\activate.bat
```



#### 🔹 Windows (PowerShell)

```
.\venv\Scripts\activate
```



> 실행 권한 에러 시:

```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```



#### 🔹 macOS

```
source venv/bin/activate
```



### 3. 라이브러리 설치 및 실행

```
pip install -r requirements.txt
```



### 4. PIP 사용 라이브러리를 추가 하여 사용 했다면 해당 라이브러리를 패키지 파일에 기록

```
pip freeze > requirements.txt
```



### 5. 서버 실행 

> uvicorn 실행때 실행 파일:FastAPI 인스턴스 --port=*** --reload

```
uvicorn main:app --port=8080 --reload
uvicorn main:app --port=8080 --workers=4 ( --workers=$(nproc) 또는 Gunicorn )
```
