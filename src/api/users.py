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

    user_sql = sqlalchemy.text("""
                               INSERT INTO users (username, level)
                               VALUES (:username, 1)
                               RETURNING user_id
                               """)
    with db.engine.begin() as connection:
        id = connection.execute(
            user_sql, {"username": username}).scalar()

    print(f"Added User:{username} with user_id: {id}")

    return [
        {
            "user_id": id,
            "success": "Successfully added user to database"
        }
    ]


@router.delete("/userDelete/", tags=["userDelete"])
def delete_user(user_id: str = ""):

    delete_sql = sqlalchemy.text("DELETE FROM users WHERE user_id = :user_id ")

    with db.engine.begin() as connection:
        connection.execute(delete_sql, {"user_id": user_id})

    print(f"Successfully deleted user: {user_id}")

    return {"success": "Successfully deleted user from database"}


@router.put("/userUpdate/", tags=["userUpdate"])
def update_user_level(user_id: int, username: str = None, level: int = None):

    update_sql = sqlalchemy.text("""
                                 update
                                     users
                                 set
                                     username = coalesce(:username, username),
                                     level = coalesce(:level, level)
                                 where
                                 user_id = :user_id
                                 returning
                                     username,
                                     level
                                 """)
    with db.engine.begin() as connection:
        result = connection.execute(update_sql, {
                                  "user_id": user_id,
                                  "username": username,
                                  "level": level}).fetchone()
        if result is None:
            return {"error": "User not found"}

    result_string = f"Successfully updated user: {result.username} to level: {result.level}"
    print(result_string)

    return {"success": result_string}


@router.put("/userLogin/", tags=["userLogin"])
def login_user(user_id: int):

    login_sql = sqlalchemy.text("""
                                update users
                                set
                                    online = true
                                where
                                    user_id = :user_id
                                returning
                                    username,
                                    online
                                """)

    with db.engine.begin() as connection:
        result = connection.execute(login_sql, {"user_id": user_id}).fetchone()
        print(result)

        if result is None:
            return {"error": "Character not found"}

    result_string = f"Successfully changed online status of {result.username} to {result.online}"
    print(result_string)

    return {"success": result_string}


@router.put("/userLogout/", tags=["userLogout"])
def logout_user(user_id: int):
    login_sql = sqlalchemy.text("""
                            update users
                            set
                                online = false
                            where
                                user_id = :user_id
                            returning
                                username,
                                online
                            """)

    with db.engine.begin() as connection:
        result = connection.execute(login_sql, {"user_id": user_id}).fetchone()

        if result is None:
            return {"error": "Character not found"}

    result_string = f"Successfully changed online status of {result.username} to {result.online}"
    print(result_string)

    return {"success": result_string}
