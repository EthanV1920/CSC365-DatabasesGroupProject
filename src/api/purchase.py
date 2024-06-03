from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
from enum import Enum
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/carts",
    tags=["cart"],
    dependencies=[Depends(auth.get_api_key)],
)


class Customer(BaseModel):
    username: str
    level: str
    bank: int


@router.post("/")
def create_cart(new_cart: Customer):
    """ """
    with db.engine.begin() as conn:
        id = conn.execute(sqlalchemy.text("SELECT user_id from users where username = :Username"),
                          {"Username": new_cart.username}).scalar()
        cartID = conn.execute(sqlalchemy.text(
            "INSERT INTO carts (user_id) VALUES (:id) RETURNING cart_id"), {"id": id}).scalar()
    return {"cart_id": cartID}


@router.post("/{cart_id}/items/{character_sku}")
def add_to_cart(cart_id: int, character_name: str):
    """ """
    with db.engine.begin() as conn:
        userID = conn.execute(sqlalchemy.text(
            "SELECT user_id FROM carts WHERE cart_id = :cartID"), [{"cartID": cart_id}]).scalar()
        characterID = conn.execute(sqlalchemy.text(
            "SELECT character_id FROM characters WHERE name = :Name"), {"Name": character_name})
        conn.execute(sqlalchemy.text("INSERT INTO cart_items (cart_id, user_id, character_id) VALUES (:cartID, :userID, :characterID)"),
                     [{"cartID": cart_id, "customerID": userID, "sku": characterID}])
    return "Added to Cart"


class CartCheckout(BaseModel):
    payment: str


@router.post("/{cart_id}/checkout")
def checkout(cart_id: int, cart_checkout: CartCheckout):
    with db.engine.begin() as conn:
        total_paid = 0
        total_bought = 0
        done = conn.execute(sqlalchemy.text(
            "SELECT checkout from cart where cart_id = :cartID"), {"cartID": cart_id})
        if not done:
            items = conn.execute(sqlalchemy.text("""SELECT cart_items.character_id as characterID, characters.price as Price, user_id as userID
                                                    FROM cart_items 
                                                    JOIN carts ON cart_items.cart_id = carts.cart_id 
                                                    JOIN characters ON characters.character_id = cart_items.character_id
                                                    WHERE carts.cart_id = :cartID"""),
                                 {"cartID": cart_id})
            for item in items:
                character, price, user = item.characterID, item.Price, item.userID
                total_bought += 1
                total_paid += price
                conn.execute(sqlalchemy.text("""INSERT INTO characters_ledger (user_id, character_id)
                                                VALUES(:userID, :characterID)"""),
                             [{"userID": user, "characterID": character}])
            conn.execute(sqlalchemy.text("INSERT INTO gold_ledger (gold) VALUES (:total_paid)"),
                         {"total_paid": total_paid})
    return {"total_potions_bought": total_bought, "total_gold_paid": total_paid}
