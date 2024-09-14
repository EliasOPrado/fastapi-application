from typing import Optional
from pydantic import BaseModel, Field


class PurchaseIn(BaseModel):
    id: int
    item: str
    price: float

class ReportIn(BaseModel):
    id: int
    title: str
    status: str

class UserIn(BaseModel):
    name: str
    email: str
    role: str