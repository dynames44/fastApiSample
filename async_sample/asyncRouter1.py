import time
import asyncio
from fastapi import APIRouter

router = APIRouter(prefix="/async1"  ,include_in_schema=False ,tags=["asynchronous Exam"])

async def long_running_task():
    await asyncio.sleep(10)        
    print("end Of Job")
    
@router.get("/task")
async def run_task():
    await long_running_task()
    return {"status": "long_running task completed"}

@router.get("/task1")
def run_task():
    time.sleep(10)
    return {"status": "long_running task completed"}

@router.get("/task2")
async def run_task():
    asyncio.create_task(long_running_task()) #back 처리 
    return {"status": "long_running task completed"}

@router.get("/quick")
async def quick_response():
    return {"status": "quick response"}
