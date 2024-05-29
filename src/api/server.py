from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
# from src.api import carts, catalog, bottler, barrels, admin, info, inventory
from src.api import characters, shop, users, match, purchase, ai
import json
import logging
import sys
from starlette.middleware.cors import CORSMiddleware

description = """
The premiere place to view all the information you could ever want on Mortal Kombat.
"""

app = FastAPI(
    title="Mortal DB",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Ethan Vosburg",
        "email": "evosburg@calpoly.edu",
    },
)

# TODO: Change to project specific
# origins = ["https://potion-exchange.velupierce@calpoly.edurcel.app"]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(ai.router)
app.include_router(characters.router)
app.include_router(shop.router)
app.include_router(users.router)
app.include_router(match.router)
app.include_router(purchase.router)
# app.include_router(carts.router)
# app.include_router(catalog.router)
# app.include_router(bottler.router)
# app.include_router(barrels.router)
# app.include_router(admin.router)
# app.include_router(info.router)


@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)


@app.get("/")
async def root():
    return {"message": "Welcome to Mortal DB"}
