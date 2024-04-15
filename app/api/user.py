from flask import request, jsonify,Blueprint
from ..services.user_service import add_user, login_user, get_user_details
import logging

user_bp = Blueprint("user", __name__,url_prefix="/user")
logger = logging.getLogger(__name__)

@user_bp.route("/register", methods=["POST"])
def register():
    logger.info("Registering new user")
    user_details = request.json
    if not user_details:
        payload = {
            "status":"failure",
            "error": "User data not supplied or is in incorrect format"
        }
        return jsonify(payload), 400
    try:
        add_user(user_details)
        return jsonify({"status": "success", "message": "User registration successful"}), 201
    except Exception as e:
        error = str(e)
        logger.error("Error registering user", exc_info=True)
        return jsonify({"status": "failure", "message": "User registration failed"}), 400

        

@user_bp.route("/login", methods=["POST"])
def login():
    login_details = request.json
    try:
        response = login_user(login_details=login_details)
        return jsonify({"status": "success", "message" : "User login successful", "data" : response}), 200
    except Exception as e:
        logger.error("Error logging in user", exc_info=True)
        return jsonify({"status": "failure", "message": "User login failed", "error": str(e)}), 400
    
@user_bp.route("/user/<int:user_id>", methods=["GET"])
def login(user_id):
    login_details = request.json
    try:
        user = get_user_details(user_id)
        if user is None:
            return jsonify({"status": "failure", "message": "User not found", "error": str(e)}), 400
        return jsonify({"status": "success", "message" : "Successfully retrieved user", "data" : user}), 200
    except Exception as e:
        logger.error("Error logging in user", exc_info=True)
        return jsonify({"status": "failure", "message": "User not found", "error": str(e)}), 400