from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.inventory import Inventory
from app.schemas.inventory import InventoryData

"""
  Inventory operations

"""


# Check if item exists in the inventory
# If not, raise exception
def get_existing_item(db: Session, item_id: int):
    item_exist = db.query(Inventory).filter(Inventory.item_id == item_id).first()
    if item_exist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in inventory"
        )

    return item_exist


# Check if item is available in required quantity
# If not, raise exception
def ensure_required_quatity_is_available(db: Session, item_id: int, q: int):
    available_item = (
        db.query(Inventory)
        .filter(and_(Inventory.item_id == item_id, Inventory.item_quantity >= q))
        .first()
    )
    if available_item is None:
        raise HTTPException(status_code=404, detail="Item out of stock")


# Get all items from the inventory.
def get_items(db: Session, offset: Optional[int] = 0, limit: Optional[int] = 20):
    return db.query(Inventory).offset(offset).limit(limit).all()


# Get item by category.
def get_item_by_category(db: Session, category: str):
    return db.query(Inventory).filter(Inventory.item_category == category).all()


# Add Item
def create_item(db: Session, new_item: InventoryData):
    db_item = Inventory(**new_item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Update existing item
def update_item(db: Session, item: InventoryData, item_id: int):
    item_in_inventory = get_existing_item(db=db, item_id=item_id)

    item_in_inventory.item_name = item.item_name
    item_in_inventory.item_price = item.item_price
    item_in_inventory.item_category = item.item_category
    item_in_inventory.item_quantity = item.item_quantity

    db.commit()
    db.refresh(item_in_inventory)
    return item_in_inventory


# Delete item by id
def delete_item(db: Session, item_id: int):
    item_remove = get_existing_item(db=db, item_id=item_id)

    db.delete(item_remove)
    db.commit()
    return {"Item deleted from inventory"}
