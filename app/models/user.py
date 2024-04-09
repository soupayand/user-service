from ..database.connection import db
from ..models.role import Role
from ..models.associations import UserRole
from werkzeug.security import generate_password_hash, check_password_hash
import enum
import logging
import os


logger = logging.getLogger(__name__)

class User(db.Model):
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    date_of_birth = db.Column(db.DateTime, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    
    roles = db.relationship("Role", secondary="user_role", back_populates="users")
    
    def set_password(self, password):
        try:
            hashed_pass = hashed_pass = generate_password_hash(password, method=os.getenv("HASHING_ALGORITHM","pbkdf2:sha256"), salt_length=int(os.getenv("SALT_LENGTH","16")))
            self.password_hash = hashed_pass
        except Exception as e:
            logger.error("Error in hashing password for new user", e)
            raise ValueError("Error storing password")
    
    def is_valid_password(self, incoming_password):
        try:
            if check_password_hash(self.password_hash, incoming_password):
                return True
        except Exception as e:
            logger.error("Error in checking stored hashed password", e)
            raise ValueError("Password entered is incorrect")
        return False
    
