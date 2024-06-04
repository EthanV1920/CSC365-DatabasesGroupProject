from fastapi import APIRouter, Depends, Request
# from pydantic import BaseModel
# from src.api import auth
# from enum import Enum
import sqlalchemy

from src import database as db
from sqlalchemy import literal_column
# from typing import Dict

router = APIRouter()


@router.get("/search/", tags=["search"])
def search_characters(character_name: str = "",
                      sort_col: str = "char.name",
                      sort_order: str = "desc"):
    result = []
    if sort_col == "0":
        sort_col = "char.name"

    char_sql = sqlalchemy.text("""
                    SELECT
                        char.name,
                        char.traits_id,
                        char.character_id,
                        tra.trait_id,
                        tra.agility,
                        tra.damage,
                        tra.control
                    FROM
                        characters AS char
                    JOIN 
                        traits AS tra ON char.traits_id = tra.trait_id
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

@router.get("/dbstats/", tags=["dbstats"])
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
