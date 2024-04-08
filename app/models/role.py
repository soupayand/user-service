from ..database.connection import db
from enum import Enum

class RoleType(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    MERCHANT = "merchant"

class Role(db.Model):
    
    __tablename__ = "role"
    
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.Enum(RoleType), nullable = False, unique=True)
    description = db.Column(db.String(256), nullable = True)
    active = db.Column(db.Boolean, default=True, nullable=False)
    
    users = db.relationship("User", secondary="user_role", back_populates="roles")
    
