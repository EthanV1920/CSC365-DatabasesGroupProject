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

    with db.engine.begin() as connection:
        user_id = connection.execute("SELECT user_id FROM users WHERE username = :username", {
                                     "username": username}).fetchone()
        if user_id is None:
            return {"error": "User not found"}

        char_id = connection.execute("SELECT character_id FROM characters WHERE name = :name", {
                                     "name": character_name}).fetchone()
        if char_id is None:
            return {"error": "Character not found"}

        gold = connection.execute(
            """
                        SELECT SUM(gold) FROM gold_ledger 
                        WHERE user_id = :user_id
                        """, {"user_id": user_id}).fetchone()
        if gold < 100:
            return {"error": "Insufficient funds"}

        connection.execute(
            """
                INSERT INTO character_ledger (user_id, character_id)
                VALUES (:user_id, :character_id)
            """, {"user_id": user_id, "character_id": char_id})

        connection.execute(
            """
                INSERT INTO gold_ledger (user_id, gold)
                VALUES (:user_id, -100)
            """, {"user_id": user_id})

    return {"success": "Successfully purchased character"}
