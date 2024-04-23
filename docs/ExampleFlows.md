# Example Flows

## Inventory Updating

Avid gamer, Lucas, just leveled up. When the game ended, POST/match/end/{match_id} is called, and the XP he earned in that match pushed him into level 20. He earned 100 coins from leveling up and 15 from winning the match. He also unlocked a new character, _Pilkington the Pickle Master_. Lucas choses to try out his new character by calling POST /match/start and selecting _Pilkington the Pickle Master_ as his player.

1. Get the match information from the front end
2. Perform a game update using the `/account/game_update/{player_id}` endpoint also updating the player to level 20 in the process
3. Check if the player has earned any more items
  3.1. If the player has earned new items, add them to the account via the game update endpoint
  3.2. If the player has not earned any items, do nothing
4. Create a new match id with the `/match/start` endpoint

## Special Purchase

Gordon, a weekend gamer, wanted to buy a new variation of his favorite character, _Carl with a K_.

1. Starts by calling GET `/inventory/` to get the item id for the skin he would like to buy
2. Next he calls POST `/carts/` to get a new cart ID with ID 9
3. Then Gordon calls PUT `/carts/9/items/{Birthday Suit}`
4. Finally he calls POST `/carts/completePurchase/9` to complete checkout. Checkout takes 1000 coins from his bank, and gives him 1 Birthday Suit and 10 XP points for making a large purchase

## Account Creation

Victoria a professional gamer is wanting to make and alt account with the name _Wild Style_ and the email _dontemailme@hotmail.com_ and the region _yugoslavia_

1. The create account endpoint would be called `account/new` passing in the given details
2. Get the response form the back end
    2.1. If the response is successful then there would be no further action needed
    2.2. If the response was not successful then resend the request a maximum of 5 times with a timeout duration of 2 seconds
