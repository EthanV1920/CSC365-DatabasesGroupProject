from pathlib import Path
from fastapi import APIRouter, Depends, Request
from src.api import auth
import sqlalchemy
# from pydantic import BaseMode
# from enum import Enum

from src import database as db

router = APIRouter()


@router.get("/match/create/", tags=["match"])
def matchCreate(user_id: int, user_char: int):

    check_sql = sqlalchemy.text("""
                                select
                                id
                                from
                                matches
                                where
                                (
                                    player1 = :user_id
                                    or player2 = :user_id
                                    )
                                and status = -1
                                """)

    match_sql = sqlalchemy.text("""
                                with user_level as (select level
                    from users
                    where user_id = :user_id),
     opponent
         as (select nullif(user_id, (select player2 from matches where player2 = :user_id and player2_char is null)) as user_id
             from users,
                  user_level
             where users.level between user_level.level - 5 and user_level.level + 5
               and user_id != :user_id
               and (select online
                    from users
                    where user_id = :user_id) = true
               and online = true
             order by random()
             limit 1)
insert into
  matches (
    player1,
    player1_char,
    player2,
    player2_char,
    status
  )
values
  (
    :user_id,
    :user_char,
    (
      select
        *
      from
        opponent
    ),
    null,
    -1
  )
returning
  id,
  player2;
                                """)

    with db.engine.begin() as connection:
        # temporarily random, will add more logic in a later implementation
        # selection parameters:
        #   should be similar level
        #   must be online
        is_open_match = connection.execute(check_sql, {"user_id": user_id}).fetchone()
        print(is_open_match)

        if is_open_match is None:
            result = connection.execute(match_sql, {"user_id": user_id, "user_char": user_char}).fetchone()
        else:
            return {"error": "There is already an open match with this player"}

        # connection.execute(match_sql)
        print(f"Result: {result}")

        if result is None:
            return {"error": "Match failed to create, check status and existence of players"}


        result_string = f"Match started with {user_id} who added {result.player2}"
        print(result_string)

    return [
        {
            "match_id": result.id,
            "opponent_id": result.player2
        }
    ]


@router.put("/match/joinMatch/", tags=["match"])
def match_join(user_id: int, user_char: int):

    join_sql = sqlalchemy.text("""
                               update matches
                               set
                               player2_char = :user_char,
                               status = 0
                               where
                               player2 = :user_id
                               and status = -1
                               """)
    with db.engine.begin() as connection:
        connection.execute(join_sql, {"user_char": user_char, "user_id": user_id})

    return {"success": "Successfully joined match"}


@router.put("/match/updateWinner/", tags=["match"])
def match_end(match_status: int, match_id: int):

    check_sql = sqlalchemy.text("SELECT id FROM matches WHERE id = :match_id")

    update_sql = sqlalchemy.text("UPDATE matches SET status = :match_status WHERE id = :match_id")

    with db.engine.begin() as connection:
        match = connection.execute(check_sql, {
                                   "match_id": match_id}).scalar()
        if match is None:
            return {"error": "Match not found"}
        else:
            connection.execute(update_sql, {"match_status": match_status, "match_id": match_id})

    return {"success": f"Successfully updated match {match}"}
