import bcrypt
from app.extensions import db
from datetime import datetime,timezone

class User(db.Model):
    __tablename__="users"
    
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(120),unique=True,nullable=False,index=True)
    password=db.Column(db.String(255),nullable=False)
    name=db.Column(db.String(100),nullable=False)
    role=db.Column(db.String(20),nullable=False,default="customer")
    created_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))

    orders=db.relationship("Order",back_populates="user",lazy="dynamic")

    def set_password(self,raw_password):
        self.password=bcrypt.hashpw(
            raw_password.encode("utf-8"),bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self,raw_password):
        return bcrypt.checkpw(
                raw_password.encode("utf-8"),
                self.password.encode("utf-8")
        )
        
    def to_dict(self):
        return {
            "id":self.id,
            "email":self.email,
            "name":self.name,
            "role":self.role,
            "created_at":self.created_at.isoformat(),
        }