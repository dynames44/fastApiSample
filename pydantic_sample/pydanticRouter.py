from fastapi import APIRouter, Request
from .pydanticModel import pydanticBase1

router = APIRouter(prefix="/pydantic", include_in_schema=False)

