from pathlib import Path
from openai import OpenAI
from fastapi import APIRouter, Depends, Request
from src.api import auth
import sqlalchemy
# from pydantic import BaseModel
# from enum import Enum

from src import database as db

client = OpenAI()
router = APIRouter()

GPT_MODEL = "gpt-3.5-turbo"


@router.get("/recommendations/", tags=["recommendations"])
def getRec(story: str = ""):

    character_sql = sqlalchemy.text("""
                                    select
                                        *
                                    from
                                        characters
                                        join traits on traits.trait_id = characters.traits_id
                                    """)

    with db.engine.begin() as connection:
        characters = connection.execute(character_sql).mappings().fetchall()

    model="gpt-3.5-turbo"

    messages=[
            {
                "role": "system",
                "content": "You will be given a  users story who is trying to figure out what character they should play from Mortal Kombat 11. Assume this user is unfamiliar with the game and the different characters. You will be given a list of all of the characters along with 3 traits and rankings for each of the traits. You must recommend 3 characters that the player should try."
            },
            {
                "role": "system",
                "content": "Here is an explanation of the agility trait: This trait refers to how easy it is to move around the stage during a fight."
            },
            {
                "role": "system",
                "content": "Here is an explanation of the damage trait: This trait refers to how much damage the character can give out with each hit."
            },
            {
                "role": "system",
                "content": "Here is an explanation of the control trait: This trait refers to how simple each character's combinations and specialty hits are to execute."
            },
            {
                "role": "system",
                "content": "An example of a trait combination that would be good for a beginner player would be, high agility, medium damage, with little emphasis on control."
            },
            {
                "role": "system",
                "content": "An example of a trait combination that would be good for an advanced player would be, high control, with there being a trade off between damage and agility."
            },
            {
                "role": "system",
                "content": f"{characters}"
            },
            {
                "role": "user",
                "content": story
            }
        ]

    tools=[
            {
                "type": "function",
                "function": {
                    "name": "create_rank",
                    "description": "This function takes a rank, name, and reason and formats it into a dictionary",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "rank": {
                                "type": "integer",
                                "description": "This is how the order of the ranking of the three characters presented",
                            },
                            "name": {
                                "type": "string",
                                "description": "The name of the character that is being recommended",
                            },
                            "reason": {
                                "type": "string",
                                "description": "The stated reason for why this character fulfills the users request",
                            },
                        },
                        "required": ["rank", "name", "reason"],
                    },
                }
            }
        ]

    if story != "":
        response = chat_completion_request(messages, tools, model)
        response_message = response.choices[0].message
        print(f"This is the response string:\n{response_message}\n")
        tool_calls = response_message.tool_calls

        ranking = []
        for i, tool_call in enumerate(tool_calls):
            rank = eval(tool_call.function.arguments)['rank']
            name = eval(tool_call.function.arguments)['name']
            reason = eval(tool_call.function.arguments)['reason']
            ranking.append({"rank": rank, "name": name, "reason": reason})



        print(f"This is the ranking: {ranking}")
        return ranking
    else:
        return "OK"

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
    print(f"Generated Instul: {insult}")

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
