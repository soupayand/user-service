from ..database.connection import db

class UserRole(db.Model):
    
    __tablename__="user_role"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable = False)