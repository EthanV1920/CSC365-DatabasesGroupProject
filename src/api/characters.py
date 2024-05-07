from fastapi import APIRouter, Depends, Request
# from pydantic import BaseModel
# from src.api import auth
# from enum import Enum
import sqlalchemy

from src import database as db
# from typing import Dict

router = APIRouter()


@router.get("/search/", tags=["search"])
def search_characters(character_name: str = "",
                      sort_col: str = "0",
                      sort_order: str = "desc"):
    result = []

    previous = ""
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
                                  characters char
                              JOIN 
                                  traits tra ON char.traits_id = tra.trait_id
                              WHERE
                                  char.name = :name
                              ORDER BY
                                  :sort_col
                                  :sort_order
                              """)

    # if character_name != "":
        # query += " WHERE char.name = :name"
        # params["name"] = character_name

    # if not search_page:
    #     search_page = "1"

    # params["page"] = search_page


    # if sort_col == "":
    #     sort_col = "char.character_id"

    # if sort_order == "":
    #     sort_order = "desc"

    # query += f" ORDER BY {sort_col} {sort_order}"

    # if character_name != "":
    #     count_query += " WHERE cust.name = :name"
    params = {
            'name': character_name,
            'sort_col': sort_col,
            'sort_order': sort_order}


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
