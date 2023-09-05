from typing import Dict, Optional

import bcrypt
from flask import Blueprint, Response, request, jsonify

from utils import get_database_connection

user = Blueprint('user', __name__)


def create_user(user_email: str, user_password: str) -> None:
    """Creates user in the database"""

    hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())
    insert_query = f"INSERT INTO users (email, password) VALUES (%s, %s);"
    insert_values = (user_email, hashed_password)

    connection = get_database_connection()
    if connection is None:
        print("ERROR: Could not connect to database")
        return None

    cursor = connection.cursor(dictionary=True)
    if cursor is None:
        print("ERROR: Could not get cursor from database connection")
        return None

    cursor.execute(insert_query, insert_values)
    cursor.close()

    return None


def authenticate_user(user_email: str, user_password: str) -> Optional[Dict[str, str]]:
    """Authenticates user in the database"""

    select_query = f"SELECT user_email, password_hash FROM users WHERE email = %s;"
    select_values = (user_email,)

    connection = get_database_connection()
    if connection is None:
        print("ERROR: Could not connect to database")
        return None

    cursor = connection.cursor(dictionary=True)
    if cursor is None:
        print("ERROR: Could not get cursor from database connection")
        return None

    cursor.execute(select_query, select_values)
    user_hashes = cursor.fetchall()
    cursor.close()

    if len(user_hashes) == 0:
        print("ERROR: User not found")
        return None
    elif len(user_hashes) > 1:
        print("ERROR: Multiple users found")
        return None

    if not bcrypt.checkpw(user_password.encode('utf-8'), user_hashes[0]['password_hash'].encode('utf-8')):
        return Response("ERROR: Invalid password", status=401)

    return recipes


@user.route('/user', methods=['POST'])
def create_user() -> Response:
    """Handles all recipes for a given user"""

    user_email = request.form.get('email')
    user_password = request.form.get('password')

    if not user_email:
        return Response("ERROR: No user email provided", status=400)

    if not user_password:
        return Response("ERROR: No user password provided", status=400)

    create_user(user_email, user_password)

    return Response("User created successfully", status=200)


@user.route('/user/login', methods=['POST'])
def create_user() -> Response:
    """Handles all recipes for a given user"""

    user_email = request.form.get('email')
    user_password = request.form.get('password')

    if not user_email:
        return Response("ERROR: No user email provided", status=400)

    if not user_password:
        return Response("ERROR: No user password provided", status=400)

    create_user(user_email, user_password)

    return Response("User created successfully", status=200)



