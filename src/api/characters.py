from fastapi import APIRouter, Depends, Request
import sqlalchemy
from sqlalchemy import text, desc, asc, literal_column
from sqlalchemy.sql import selectable

from src import database as db
from sqlalchemy import literal_column
# from typing import Dict

router = APIRouter()


@router.get("/search/", tags=["search"])
def search_characters(character_name: str = "",
                      sort_col: str = "char.name",
                      sort_order: str = "desc"):
    result = []
    allowed_columns = ["char.name", "traits.agility", "traits.damage", "traits.control", "damage", "control", "agility"]
    allowed_orders = ["asc", "desc"]
    banned_characters = [";", "DROP", "TABLE", "DELETE", "UPDATE", "INSERT", "SELECT", "FROM", "WHERE", "AND", "OR", "'", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

    for char in banned_characters:
        if char in character_name:
            character_name = ""
            break

    character_name = character_name.capitalize()
        
    if sort_col not in allowed_columns:
        sort_col = "char.name"
    if sort_order not in allowed_orders:
        sort_order = "desc"


    char_sql = sqlalchemy.text("""
                    SELECT
                        char.name,
                        char.traits_id,
                        char.character_id,
                        traits.trait_id,
                        traits.agility,
                        traits.damage,
                        traits.control
                    FROM
                        characters AS char
                    JOIN 
                        traits ON char.traits_id = traits.trait_id
                    WHERE
                        char.name LIKE :name
                    ORDER BY
                        {sort_col} {sort_order}
                    """.format(sort_col=literal_column(sort_col), sort_order=sort_order))



    params = {
            'name': '%' + character_name + '%',
            }

    with db.engine.begin() as connection:
        results = connection.execute(char_sql, params).fetchall()

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

@router.get("/characterCount/", tags=["characterCount"])
def dbstats():
    stats_sql = sqlalchemy.text("""
                                SELECT
                                    count(characters.name) as count
                                from
                                    characters
                                """)

    with db.engine.begin() as connection:
        result = connection.execute(stats_sql).fetchone()

    print(f"The result count is: {result.count}")

    return result.count
