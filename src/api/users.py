from fastapi import APIRouter, Depends, Request
import sqlalchemy

from src import database as db
# from typing import Dict

router = APIRouter()


@router.get("/userNew/", tags=["userNew"])
def new_account(username: str = ""):

    user_sql = sqlalchemy.text("""
                               INSERT INTO users (username, level)
                               VALUES (:username, 1)
                               RETURNING user_id
                               """)
    with db.engine.begin() as connection:
        exists = connection.execute(sqlalchemy.text("select coalesce(user_id, 0) from users where username = :username"), {"username": username}).scalar_one()
        if (not exists):
            print("Username already in use")
            return {"Username already in use"}
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
def delete_account(user_id: str = ""):


    try:
        int(user_id)
    except ValueError:
        return {"error": "Invalid user_id"}
            
    delete_sql = sqlalchemy.text("DELETE FROM users WHERE user_id = :user_id ")

    with db.engine.begin() as connection:
        exists = connection.execute(sqlalchemy.text("select coalesce(username, NULL) from users where user_id = :user_id"), {"user_id": user_id}).fetchone()
        if (not exists):
            print("User Not Found")
            return {"User Not Found"}

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
        online = connection.execute(sqlalchemy.text("select online from users where user_id = :user_id"), {"user_id": user_id}).fetchone()
        if (online):
            return {"Already Online"}

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
        online = connection.execute(sqlalchemy.text("select online from users where user_id = :user_id"), {"user_id": user_id}).fetchone()
        if (not online):
            return {"Already Offline"}

        result = connection.execute(login_sql, {"user_id": user_id}).fetchone()

        if result is None:
            return {"error": "Character not found"}

    result_string = f"Successfully changed online status of {result.username} to {result.online}"
    print(result_string)

    return {"success": result_string}
