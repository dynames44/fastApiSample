from typing import Annotated
from .pydanticModel import Item
from pydantic import ValidationError 
from fastapi.exceptions import RequestValidationError
from fastapi import APIRouter ,Path ,Form ,Depends

router = APIRouter(prefix="/pydantic2"  ,tags=["Pydantic Model Validator Exam"])
#router = APIRouter(prefix="/pydantic2"  ,include_in_schema=False)