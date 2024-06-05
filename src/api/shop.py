from fastapi import APIRouter, Depends, Request
# from pydantic import BaseModel
# from src.api import auth
# from enum import Enum
import sqlalchemy

from src import database as db
# from typing import Dict

router = APIRouter()


@router.get("/charPurchase/", tags=["charPurchase"])
def dbstats(username: str = "",
            character_name: str = ""):
    
    banned_characters = [";", "DROP", "TABLE", "DELETE", "UPDATE", "INSERT", "SELECT", "FROM", "WHERE", "AND", "OR", "'"]

    for char in banned_characters:
        if char in username:
            username = ""
            break
        if char in character_name:
            character_name = ""
            break
    

    with db.engine.begin() as connection:
        user_id, char_id, gold = connection.execute("""
            SELECT users.user_id, characters.character_id, COALESCE(SUM(gold_ledger.gold), 0)
            FROM users
            LEFT JOIN characters ON characters.name = :character_name
            LEFT JOIN gold_ledger ON users.user_id = gold_ledger.user_id
            WHERE users.username = :username
            GROUP BY users.user_id, characters.character_id
        """, {"username": username, "character_name": character_name}).fetchone()

        if user_id is None:
            return {"error": "User not found"}
        if char_id is None:
            return {"error": "Character not found"}
        if gold < 100 or gold is None:
            return {"error": "Insufficient funds"}

        connection.execute("""
            INSERT INTO character_ledger (user_id, character_id) VALUES (:user_id, :character_id);
            INSERT INTO gold_ledger (user_id, gold) VALUES (:user_id, -100)
        """, {"user_id": user_id, "character_id": char_id})

    return {"success": "Successfully purchased character"}
