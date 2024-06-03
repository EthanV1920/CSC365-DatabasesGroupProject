from pathlib import Path
from fastapi import APIRouter, Depends, Request
from src.api import auth
import sqlalchemy
# from pydantic import BaseMode
# from enum import Enum

from src import database as db

router = APIRouter()


@router.get("/match/create/", tags=["match"])
def matchCreate(user_id: int):

    match_sql = sqlalchemy.text("""
with
  user_level as (
    select
      level
    from
      users
    where
      user_id = 2
  ),
  opponent as (
    select
      nullif(
        user_id,
        (
          select
            player2
          from
            matches
          where
            player2 = 2
            and player2_char is null
        )
      ) as user_id
    from
      users,
      user_level
    where
      users.level between user_level.level - 1 and user_level.level  + 1
      and user_id != 2
      and (
        select
          online
        from
          users
        where
          user_id = 2
      )
      and online = true
    order by
      random()
    limit
      1
  )
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
    2,
    1,
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
  player2;

do $$
    begin
        if exists(select player2 from matches where player2 = 2) then
            raise exception 'Match Already Exists';
            rollback;

        end if;
    end
$$;
                                """)

    with db.engine.begin() as connection:
        # temporarily random, will add more logic in a later implementation
        # selection parameters:
        #   should be similar level
        #   must be online
        try:
            result = connection.execute(match_sql, {"user_id": user_id}).fetchone()
        except Exception as e:
            print(f"Exception: {e}")

        # connection.execute(match_sql)
        print(f"Result: {result}")

        if result is None:
            return {"error": "Match failed to create, check status and existence of players"}


        result_string = f"Match started with {user_id} who added {result.player2}"
        print(result_string)

    return [
        {
            "match_id": "match",
            "opponent_id": "opponent"
        }
    ]


@router.put("/match/updateWinner/", tags=["match"])
def match_end(winner: int, match_id: int):
    with db.engine.begin() as connection:
        match = connection.execute("SELECT match_id FROM matches WHERE match_id = :match_id", {
                                   "match_id": match_id}).fetchone()
        if match is None:
            return {"error": "Match not found"}
        else:
            connection.execute("""
                               UPDATE matches SET result = :winner WHERE match_id = :match_id
                               """, {"winner": winner, "match_id": match_id})

    return {"success": "Successfully updated match"}
