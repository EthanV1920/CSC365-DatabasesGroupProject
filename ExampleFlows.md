Example Flows

1) Avid gamer, Lucas, just leveled up. When the game ended, POST/match/end/{match_id} is called, and the XP he earned in that match pushed him into level 20. He earned 100 coins from leveling up and 15 from winning the match. He also unlocked a new character, _Pilkington the Pickle Master_. Lucas choses to try out his new character by calling POST /match/start and selecting _Pilkington the Pickle Master_ as his player. He loves the new character and spends the rest of the night mastering his attack combinations.

2) Gordon, a weekend gamer, wanted to buy a new variation of his favorite character, _Carl with a K_. To do so he:
- starts by calling GET /inventory/ to get the amount of coins he has, and is returned Bank = 1200 coins.
- next he calls POST /carts/ to get a new cart ID with ID 9
- then Gordon calls PUT /carts/9/items/{Birthday Suit}
- finally he calls POST /carts/completePurchase/9 to complete checkout. Checkout takes 1000 coins from his bank, and gives him 1 Birthday Suit and 10 XP points for making a large purchase.
  Excited about his new purchase, Gordon plays 10 more games before calling it a night.

3)


4)

