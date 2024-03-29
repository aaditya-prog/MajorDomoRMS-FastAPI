from pydantic import BaseModel


class InventoryData(BaseModel):
    item_name: str
    item_category: str
    item_price: float
    item_quantity: str


class Item(InventoryData):
    item_id: int

    class Config:
        orm_mode = True


ItemByCategory = dict[str, list[Item]]
