from .orm_repository import orm_repository as repository

#사용자 목록 조회 
async def get_user_list(param : dict = None):
    return await repository.get_user_list(param)

#사용자 상세정보 
async def get_user_info(param : dict):
    return await repository.get_user_info(param)

#사용자 상세정보 
async def get_user_join(param : dict):
    return await repository.get_user_join(param)

class orm_usecase:
    get_user_list = staticmethod(get_user_list)
    get_user_info = staticmethod(get_user_info)    
    get_user_join = staticmethod(get_user_join)    