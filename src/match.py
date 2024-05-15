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
        #temporarily random, will add more logic in a later implementation
        opponent = connection.execute("""
            SELECT user_id FROM users WHERE online = TRUE ORDER BY RANDOM() LIMIT 1
        """).fetchone()
        user_id = connection.execute("SELECT user_id FROM users WHERE username = :username", {"username": username}).fetchone()
        match_id = connection.execute(
            """
                INSERT INTO matches (player1, player2, result)
                VALUES (:user_id, :opponent, 0)
                RETURNING match_id
            """, {"user_id": user_id, "opponent": opponent}
        )

    return [
                {
                    "match_id": match_id,
                    "opponent_id": opponent
                }
            ]