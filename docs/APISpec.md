# API Specification for Fighting Game Backend

## 1. Shop Purchase

The API calls are made in this sequence when making a purchase:

1. `Get Inventory`
2. `New Cart`
3. `Add Item to Cart` (Can be called multiple times)
4. `Make Purchase`

### 1.1. Get Inventory - `/inventory/` (GET)

Get the catalog of available items that the player can buy with all the attributes

**Response**:

```json
[
  {
    "item_name": "string",
    "item_sku": "string",
    "price": "integer"
  },
  {
    ...
  }
]
```

### 1.2. New Cart - `/carts/` (POST)

Creates a new cart for a specific customer.

**Request**:

```json
{
  "player_id": "integer",
  "inventory_id": "integer",
}
```

**Response**:

```json
{
    "cart_id": "string" /* This id will be used for future calls to add items and checkout */
}
```

### 1.2. Add Item to Cart - `/carts/{cart_id}/items/{item_sku}` (PUT)

Updates the quantity of a specific item in a cart.

**Request**:

```json
{
  "item_id": "integer"
}
```

**Response**:

```json
{
    "success": "boolean"
}
```

### 1.4. Make Purchase - `/carts/completePurchase/{cart_id}` (POST)

Uses the inventory to determine if a purchase is viable and if so updates the inventory to reflect the purchase

**Request**:

```json
[
  {
    "item_sku": "sting",
    "price": "integer"
  },
  {
    ...
  }
]
```

**Response**:

```json
{
    "success": "boolean"
}
```

## 2. Match Handling

The API calls are made in this sequence when the matches happen:

1. `Start Match`
2. `End Match`

### 2.1. Start Match - `/match/start/` (POST)

Runs an algorithm to match you up with a properly skilled opponent

**Response**:

```json
[
    {
        "match_id": "integer",
        "opponent_id": "integer"
    }
]
```

### 2.2. End Match - `/match/end/{match_id}` (POST)

Ends the match updating match table with who won and who lost

**Response**:

```json
[
    {
        "success": "boolean",
        "winner": "player_id",
        "loser": "player_id"
    }
]
```

## 3. Account Handling

The API calls are made that manage account activities:

1. `New Account`
2. `Delete Account`
3. `Game Update Account`

### 3.1. New Account - `/account/new` (POST)

Gets the plan for purchasing wholesale barrels. The call passes in a catalog of available barrels
and the shop returns back which barrels they'd like to purchase and how many.

**Request**:

```json
[
  {
    "username": "string",
  }
]
```

**Response**:

```json
[
    {
        "user_id": "integer",
        "success": "str"
    }
]
```

### 3.2. Delete account - `/account/delete/{user_id}` (POST)

Deletes the entire account from the database

**Request**:

```json
[
  {
    "Success": "str"
  }
]
```


### 3.3 Game Update Level - `/account/game_update/{user_id}` (POST)

Allow the game to update player attributes as they win and lose games will take in the gains and losses and then reflect those changes in the database.

**Request**:

```json
[
  {
    "username": "string",
    "level": "integer"
  }
]
```

**Response**:

```json
[
  {
    "success": "boolean"
  }
]
```
