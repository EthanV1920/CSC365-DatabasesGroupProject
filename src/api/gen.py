from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
from enum import Enum
import sqlalchemy
from src import database as db
from faker import Faker


router = APIRouter()

@router.get("/datagen/", tags=["datagen"])
def datagen():
    result = []
    fake = Faker(['it_IT', 'en_US', 'de_DE', 'fr_FR', 'es_ES', 'nl_NL', 'pt_PT'])
    for _ in range(10):
        name = fake.name()
        level = fake.random_int(min=1, max=100)
        print(name, level)
        result.append = fake.name(), level
    
    return result.count