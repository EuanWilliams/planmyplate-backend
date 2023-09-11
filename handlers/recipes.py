from typing import Dict, Optional
from flask import Blueprint, Response, jsonify

from utils.utils import get_database_connection
from utils.local_typing import API_Response

recipes = Blueprint("recipes", __name__)


def get_recipe(user_id: int) -> Optional[Dict[str, str]]:
    """Returns all recipes available to a single user"""

    select_query = f"""
        SELECT * FROM recipes 
        WHERE id IN (SELECT recipe_id FROM user_recipes WHERE user_id = %s);
    """
    select_values = (user_id,)

    connection = get_database_connection()
    if connection is None:
        print("ERROR: Could not connect to database")
        return None

    cursor = connection.cursor(dictionary=True)
    if cursor is None:
        print("ERROR: Could not get cursor from database connection")
        return None

    cursor.execute(select_query, select_values)
    recipes = cursor.fetchall()
    cursor.close()

    return recipes


@recipes.route("/recipes/<string:user_id>/", methods=["GET"])
def all_user_recipes(user_id: str) -> API_Response:
    """Handles all recipes for a given user"""

    print(f"INFO: Received request for all recipes for user {user_id}")

    if not user_id:
        return Response("ERROR: No user id provided", status=404)

    if not user_id.isdigit():
        return Response("ERROR: Invalid user id provided", status=400)

    recipes = get_recipe(int(user_id))
    if recipes is None:
        return Response("ERROR: Could not retrieve recipes from database", status=500)
    elif not recipes:
        return Response("No recipes found for user", status=200)

    print(recipes)

    return jsonify(recipes), 200
