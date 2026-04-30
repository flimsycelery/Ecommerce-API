from app.extensions import db
from datetime import datetime,timezone

class Order(db.Model):
    __tablename__="orders"
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False,index=True)
    status=db.Column(db.String(50),nullable=False,default="pending")
    total=db.Column(db.Float,nullable=False,default=0.0)
    created_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))
    updated_at=db.Column(db.DateTime,default=lambda: datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc))

    user=db.relationship("User",back_populates="orders")
    items=db.relationship("OrderItem",back_populates="order",cascade="all,delete-orphan")

    def calculate_total(self):
        self.total=sum(item.quantity*item.unit_price for item in self.items)

    def to_dict(self):
        return {
            "id":self.id,
            "user_id":self.user_id,
            "status":self.status,
            "total":self.total,
            "items":[item.to_dict() for item in self.items],
            "created_at":self.created_at.isoformat(),
        }
    
class OrderItem(db.Model):
    __tablename__="order_items"

    id=db.Column(db.Integer,primary_key=True)
    order_id=db.Column(db.Integer,db.ForeignKey("orders.id"),nullable=False)
    product_id=db.Column(db.Integer,db.ForeignKey("products.id"),nullable=False)
    quantity=db.Column(db.Integer,nullable=False,default=1)
    unit_price=db.Column(db.Float,nullable=False)

    order=db.relationship("Order",back_populates="items")
    product=db.relationship("Product",back_populates="order_items")

    def to_dict(self):
        return {
            "product_id":self.product_id,
            "product_name":self.product.name,
            "quantity":self.quantity,
            "unit_price":self.unit_price,
            "subtotal":self.quantity*self.unit_price,
        }