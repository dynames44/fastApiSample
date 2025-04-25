from fastapi import APIRouter, Query,Depends, Body
from typing import Annotated, Optional
from .orm_model import serch_model, find_user, sys_user, user_etc

router = APIRouter(prefix="/orm"  ,tags=["DB ORM Exam"])