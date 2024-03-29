from sqlalchemy import Column, Date, func, Integer, JSON, String

from app.config.database import Base
from app.schemas.order import Status


class Orders(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    items = Column(JSON, nullable=False)
    order_date = Column(Date, server_default=func.now())
    table = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default=Status.RECEIVED)
    note = Column(String)

    def dict(self):
        return {
            "items": self.items,
            "table": self.table,
            "order_id": self.order_id,
            "order_date": self.order_date,
            "status": self.status,
            "note": self.note
        }
