from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, MultipleResultsFound
from .orm_entity import SysUser, UserEtc
from core.orm_util import get_db_session, set_exec_result, get_db_commit_session

#사용자 목록 조회 
async def get_user_list(params: dict):
    try:
        Session = get_db_session()
        
        with Session() as session:
            stmt = select(SysUser)

            if params.get("use_yn"):
                stmt = stmt.where(SysUser.use_yn == params["use_yn"])

            if params.get("email"):
                stmt = stmt.where(SysUser.email.like(f"%{params['email']}%"))

            stmt = stmt.order_by(SysUser.user_id)
            
            # # 페이징 적용
            # page = params.get("page", 1)         # 요청 파라미터로 page 받기 (기본 1페이지)
            # size = params.get("size", 10)         # 요청 파라미터로 size 받기 (기본 10개씩)

            # offset = (page - 1) * size
            # stmt = stmt.offset(offset).limit(size)            

            result = session.execute(stmt)
            data_list = result.scalars().all()
            
            if len(data_list) < 1 :
                rtnResult = set_exec_result("Error" ,"조회된 건이 없습니다." ,0 ,"")
            
            else:
                rtnResult = set_exec_result("Success" ,"" ,len(data_list) ,[data.to_dict() for data in data_list])       
                
            return rtnResult     

    except SQLAlchemyError as e:
        print("DB 조회 오류:", e)
        rtnResult = set_exec_result("Error", f"쿼리 실행 오류: {e}", 0)
        return rtnResult

#사용자 상세정보     
async def get_user_info (params : dict) :
    
    try:
        Session = get_db_session()
        
        with Session() as session:

            try:    
                stmt = select(SysUser)
                stmt = stmt.where(SysUser.user_id == params["user_id"])

                result = session.execute(stmt)
                data = result.scalar_one_or_none()
                
                if data is None :
                    rtnResult = set_exec_result("Error" ,"조회된 건이 없습니다." ,0 ,"")
                
                else:
                    rtnResult = set_exec_result("Success" ,"" ,0 ,data.to_dict())       
                    
            except MultipleResultsFound as e:
                rtnResult = set_exec_result("Error", f"쿼리 실행 오류: {e}", 0)

    except SQLAlchemyError as e:
        print("DB 조회 오류:", e)
        rtnResult = set_exec_result("Error", f"쿼리 실행 오류: {e}", 0)
    
    return rtnResult     

#사용자 정보 + 기타 정보 : Join  
async def get_user_join(params: dict):
    try:
        Session = get_db_session()

        with Session() as session:
            
            user_etc_dict = UserEtc().to_dict()
            user_etc_dict.pop("user_id", None)
            
            stmt = select(SysUser, UserEtc).outerjoin(UserEtc, SysUser.user_id == UserEtc.user_id) #Left Outer Join 
            #stmt = select(SysUser, UserEtc).join(UserEtc, SysUser.user_id == UserEtc.user_id) # Inner Join 

            # 조건 추가
            if params.get("user_id"):
                stmt = stmt.where(SysUser.user_id == params["user_id"])

            if params.get("use_yn"):
                stmt = stmt.where(SysUser.use_yn == params["use_yn"])

            if params.get("email"):
                stmt = stmt.where(SysUser.email.like(f"%{params['email']}%"))

            stmt = stmt.order_by(SysUser.user_id)

            # 실행
            result = session.execute(stmt)
            rows = result.all()

            if len(rows) < 1:
                rtnResult = set_exec_result("Error", "조회된 건이 없습니다.", 0, "")
            else:
                # (SysUser, UserEtc) 튜플로 넘어오기 때문에 풀어야 함
                rtnResult = set_exec_result(
                    "Success",
                    "",
                    len(rows),
                    [
                        # 동일한 필드명은 뒤에쓴걸로 덮어써진다.
                        {
                            **(user_etc.to_dict() if user_etc else user_etc_dict),  # None이면 가짜 객체로 대체
                            **sys_user.to_dict()
                        }
                        # 모델객체 분리 처리.
                        # {
                        #    "sys_user": sys_user.to_dict(),
                        #    "user_etc": user_etc.to_dict() if user_etc else user_etc_dict
                        # }
                        for sys_user, user_etc in rows
                    ]
                )

            return rtnResult

    except SQLAlchemyError as e:
        print("DB 조회 오류:", e)
        rtnResult = set_exec_result("Error", f"쿼리 실행 오류: {e}", 0)
        return rtnResult

class orm_repository:
    get_user_list = staticmethod(get_user_list)
    get_user_info = staticmethod(get_user_info)
    get_user_join = staticmethod(get_user_join)