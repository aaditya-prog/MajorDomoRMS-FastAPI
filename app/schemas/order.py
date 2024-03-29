from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator

from app.schemas.food import Food


class OrderItems(BaseModel):
    food: Food
    quantity: int


class OrderBase(BaseModel):
    items: list[OrderItems]
    table: int
    note: Optional[str]

    @validator("table")
    def table_is_valid(cls, v):
        if v < 1 or v > 8:
            raise ValueError("Not a valid table number")
        return v


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    items: list[OrderItems]


class Status(str, Enum):
    RECEIVED = "Received"
    PREPARING = "Preparing"
    PREPARED = "Prepared"
    PAID = "Paid"
    CANCELLED = "Cancelled"


class Order(OrderBase):
    order_id: int
    order_date: date
    status: Status
