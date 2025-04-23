from .sample_repository import sample_repository as repository

async def single_query(param : dict = None):
    return await repository.single_query(param)

class usecase:
    single_query = staticmethod(single_query)