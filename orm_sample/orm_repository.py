from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from orm_entity import SysUser, UserEtc
from core.orm_util import get_db_session, set_exec_result, get_db_commit_session

def get_user_list(params: dict):
    try:
        Session = get_db_session()
        with Session() as session:
            stmt = select(SysUser)

            if params.get("use_yn"):
                stmt = stmt.where(SysUser.use_yn == params["use_yn"])

            if params.get("email"):
                stmt = stmt.where(SysUser.email.like(f"%{params['email']}%"))

            stmt = stmt.order_by(SysUser.user_id)

            result = session.execute(stmt)
            data_list = result.scalars().all()
            
            #rtn_data = 

            return [data.to_dict() for data in data_list]

    except SQLAlchemyError as e:
        print("DB 조회 오류:", e)
        return []
