import openai as OpenAI
from pathlib import Path
from fastapi import APIRouter, Depends, Request
from src.api import auth
import sqlalchemy
# from pydantic import BaseMode
# from enum import Enum

from src import database as db

# client = OpenAI()
GPT_MODEL = "gpt-3.5-turbo"

router = APIRouter()


@router.get("/userNew/", tags=["userNew"])
def dbstats(username: str = ""):

    with db.engine.begin() as connection:
        # temporarily random, will add more logic in a later implementation
        opponent = connection.execute("""
            SELECT user_id FROM users WHERE online = TRUE ORDER BY RANDOM() LIMIT 1
        """).fetchone()
        user_id = connection.execute("SELECT user_id FROM users WHERE username = :username", {
                                     "username": username}).fetchone()
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


@router.put("/match/updateWinner/", tags=["matchUpdate"])
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


@router.get("/insult/", tags=["insult"])
def getInsult(player: str = "", game_end_state: str = "", opponent: str = ""):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful ai that will assist a user who is playing Mortal Kombat 11 in insulting their opponent in a tongue-in-cheek way. You will be given the oponents name and weather or not the user won as well as the player that the user was using. You must create an insult that is witty and funny that can be put though a text to speech program and be said out loud. The response should only contain the insult."
        },
        {
            "role": "user",
            "content": f"My player was {player} and I {game_end_state} the match, my opponent was {opponent}. Can you help me come up with a funny insult that I could tell the person who I played with?"
        }

    ]

    insult = chat_completion_request(messages)

    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=insult
            )

    response.stream_to_file(speech_file_path)

    return insult


def chat_completion_request(messages, tools=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e
