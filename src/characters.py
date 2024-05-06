from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
from enum import Enum
import sqlalchemy
from src import database as db
from typing import Dict

@router.get("/search/", tags=["search"])
def search_characters(
        character_name: str = "",
        sort_col: str = "",
        sort_order: str = "",
    ):
        result = []

            
        previous = ""
        query = """
            SELECT char.name, char.traits_id, char.character_id, tra.trait_id, tra.agility, tra.damage, tra.control
            FROM characters char
            JOIN traits tra ON char.traits_id = tra.trait_id
        """
        
        params = {}
        if character_name != "":
            query += " WHERE char.name = :name"
            params["name"] = character_name


            
        if not search_page:
            search_page = "1"
        
        params["page"] = search_page
        
            
        if sort_col == "":
            sort_col = "char.character_id"
        if sort_order == "":
            sort_order = "desc"
            
        query += f" ORDER BY {sort_col} {sort_order}"
        

        if character_name != "":
            count_query += " WHERE cust.name = :name"

        with db.engine.begin() as connection:
            results = connection.execute(sqlalchemy.text(query), params).fetchall()
        
        for row in results:
            result.append({
                "Character Name": row.name,
                "Character Id": row.character_id,
                "Agility": row.agility,
                "Damage": row.damage,
                "Control": row.control
            })

        return {
            "results": result
        }