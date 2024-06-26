from ..models.user import User, Role
from ..database.connection import db
from cachetools import TTLCache

import os
import logging
import jwt
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
cache = TTLCache(maxsize=100, ttl=900)
_DEFAULT_ROLE = "customer"

def validate_user_details(user_details):
    required_keys = ["first_name", "email", "password"]
    incoming_keys = user_details.keys()
    for key in required_keys:
        if key not in incoming_keys:
            raise KeyError("Payload doesn't contain the required keys")
    pass
    
def add_user(user_details):
    try:
        validate_user_details(user_details)
        first_name, email, password, role = user_details.values()
        if first_name is None or email is None or password is None or role is None or role.lower() == "admin":
            raise ValueError("Missing values for user details")
        role = Role.query.filter_by(type=role.upper()).first()
        if role is None:
            raise ValueError("Error in assigning role")
        new_user = User()
        new_user.first_name = first_name
        new_user.email = email
        new_user.set_password(password=password)
        new_user.roles.append(role)
        db.session.add(new_user)
        db.session.commit()
        logger.info("New user added", extra={"user":user_details})
    except KeyError as e:
        logger.error("Error adding user", e)
        raise e
    except Exception as e:
        logger.error("Error adding user to the database")
        db.session.rollback()
        raise e
    
def login_user(login_details) -> dict:
        try:
            if "email" not in login_details.keys() or "password" not in login_details.keys():
                raise KeyError("Login payload doesn't contain email or password")
            email = login_details["email"]
            user = retrieve_user_details(email=email)
            password = login_details["password"]
            valid_pass = user.is_valid_password(password)
            if not valid_pass:
                logger.error("User entered wrong password", extra={"user":user})
                raise ValueError("Entered password is wrong")
            token =   generate_jwt(user.id, user.email)
            payload = {
                "token" : token,
                "expires_in" : 60 * int(os.getenv("TOKEN_EXPIRATION_TIME",15)),
                "token_type" : "Bearer"
            }
            return payload
        except KeyError or NameError as e:
            logger.error("Invalid login credentials")
            raise e
    
def retrieve_user_details(email=None, user_id=None) -> User:
    if email is None and user_id is None:
        raise ValueError("Either email or user_id must be provided")

    key = email if email is not None else user_id
    attribute = 'email' if email is not None else 'id'

    user = cache.get(key)
    if user is None:
        logger.info("Cache miss : User", extra={attribute: key})
        filter_by_args = {attribute: key}
        user = User.query.filter_by(**filter_by_args).first()
        if user is None:
            raise NameError(f"User with {attribute} '{key}' doesn't exist")

        cache[key] = user
        logger.info(f"Fetched user details for user from database", extra={"user": user})
    else:
        logger.info("Cache hit : User", extra={attribute: key})
        
    return user

    
def generate_jwt(user_id, email) -> str:
        expiration_time = datetime.utcnow() + timedelta(minutes=int(os.getenv("TOKEN_EXPIRATION_TIME",15)))
        payload = {
            "user_id": user_id,
            "email" : email,
            "exp" : expiration_time
        }
        secret_key = os.getenv("JWT_SECRET_KEY")
        algo = os.getenv("JWT_HASHING_ALGORITHM")
        if secret_key is None:
            logger.error("JWT_SECRET_KEY not found in environment")
            raise ValueError("Error in token generation")
        return jwt.encode(payload, secret_key, algorithm=algo) 

    
    
    
    


    
        
        



    
    