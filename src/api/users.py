from fastapi import APIRouter, Depends, Request
# from pydantic import BaseModel
# from src.api import auth
# from enum import Enum
import sqlalchemy

from src import database as db
# from typing import Dict

router = APIRouter()

@router.get("/userNew/", tags=["userNew"])
def dbstats(username: str = ""):
    
    with db.engine.begin() as connection:
        name = connection.execute("SELECT name FROM users WHERE username = :username", {"username": username}).fetchone()
        if name is None:
            return {"error": "User not found"}
        else:
            id = connection.execute("""
                               INSERT INTO users (username, level)
                               VALUES (:username, 1)
                               RETURNING user_id
                               """
                               , {"username": username}).fetchone()

    return [
                {
                    "user_id": id,
                    "success": "Successfully added user to database"
                }
            ]

    
@router.delete("/userDelete/", tags=["userDelete"])
def delete_user(username: str = ""):
    with db.engine.begin() as connection:
        user = connection.execute("SELECT name FROM users WHERE username = :username", {"username": username}).fetchone()
        if user is None:
            return {"error": "User not found"}
        else:
            connection.execute("""
                               DELETE FROM users WHERE username = :username
                               """, {"username": username})

    return {"success": "Successfully deleted user from database"}

@router.put("/userUpdate/", tags=["userUpdate"])
def update_user_level(username: str = "", level: int = 1):
    with db.engine.begin() as connection:
        user = connection.execute("SELECT name FROM users WHERE username = :username", {"username": username}).fetchone()
        if user is None:
            return {"error": "User not found"}
        else:
            connection.execute("""
                               UPDATE users SET level = :level WHERE username = :username
                               """, {"username": username, "level": level})

    return {"success": "Successfully updated user's level"}


@router.put("/userLogin/", tags=["userLogin"])
def login_user(username: str = ""):
    with db.engine.begin() as connection:
        user_id = connection.execute("SELECT user_id FROM users WHERE name = :name", {"name": username}).fetchone()
        if user_id is None:
            return {"error": "Character not found"}
        else:
            connection.execute("""
                               UPDATE characters SET online = TRUE WHERE user_id = :user_id
                               """, {"user_id": user_id})

    return {"success": "Successfully logged in user"}

@router.put("/userLogout/", tags=["userLogout"])
def logout_user(username: str = ""):
    with db.engine.begin() as connection:
        user_id = connection.execute("SELECT user_id FROM users WHERE name = :name", {"name": username}).fetchone()
        if user_id is None:
            return {"error": "User not found"}
        else:
            connection.execute("""
                               UPDATE characters SET online = FALSE WHERE user_id = :user_id
                               """, {"user_id": user_id})

    return {"success": "Successfully logged out user"}