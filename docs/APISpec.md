# API Specification for Fighting Game Backend

## 1. Shop Purchase

The API calls are made in this sequence when making a purchase:

1. `Search Characters`
2. `New Cart`
3. `Add Item to Cart` (Can be called multiple times)
4. `Make Purchase`

### 1.1.Search Characters- `/characters/search_characters/` (GET)

Get the catalog of available items that the player can buy with all the attributes

**Query Parameters**:

- `character_name` (optional): The name of the character.
- `sort_col` (optional): The column to sort the results by. Possible values: `char.name` (character name), `traits.agility`, `traits.damage`, `traits.control`, `damage`, `control`, `agility`. Default: `char.name`.
- `sort_order` (optional): The sort order of the results. Possible values: `asc` (ascending), `desc` (descending). Default: `desc`.

**Response**:

The API returns a JSON object with the following structure:

- `results`: An array of objects, each representing a line item. Each line item object has the following properties:
    - `Character Name`: Astring that represents the characters name.
    - `Character Id`: An integer that represents characters identifier.
    - `Agility`: An integer that represents characters agility level.
    - `Damage`: An integer that represents characters damage level.
    - `Control`: An integer that represents characters control level.

### 1.2. New Cart - `/purchase/` (POST)

Creates a new cart for a specific user.

**Request**:

```json
{
  "username": "string"
}
```

**Response**:

```json
{
    "cart_id": "integer" /* This id will be used for future calls to add items and checkout */
}
```

### 1.2. Add Item to Cart - `/purchase/{cart_id}/items/{item_sku}` (POST)

Updates the quantity of a specific item in a cart.

**Request**:

```json
{
  "cart_id": "integer",
  "character_name": "string"
}
```

**Response**:

```json
{
    "Added to cart": "boolean"
}
```

### 1.4. Checkout - `/carts/completePurchase/{cart_id}` (POST)

Uses the inventory to determine if a purchase is viable and if so updates the inventory to reflect the purchase

**Request**:

```json
[
  "cart_id": "int",
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

1. `Create Match`
2. `End Match`

### 2.1. Match Create - `/match/create/` (POST)

Runs an algorithm to match you up with an opponent

**Request**
```json
{
    "user_id": "int"
}
```

**Response**:

```json
[
    {
        "match_id": "integer",
        "opponent_id": "integer"
    }
]
```

### 2.2. End Match - `/match/updateWinner/` (POST)

Ends the match updating match table with who won and who lost

**Response**:

```json
[
    {
        "winner": "player_id",
        "match_id": "integer"
    }
]
```

## 3. Account Handling

The API calls are made that manage account activities:

1. `New Account`
2. `Delete Account`
3. `Game Update Account`
4. `Log on`
5. `Log off`

### 3.1. New Account - `/userNew/` (POST)

Cretes a new ccount for user, given username. Only makes account for unique usernames

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
        "success: Successfully added user to database"
    }
]
```

### 3.2. Delete account - `/userDelete/` (POST)

Deletes the entire account from the database

**Request**:

```json
[
  {
    "user_id_": "string"
  }
]
```


### 3.3 Game Update Level - `/userUpdate/` (POST)

Allow the game to update player attributes as they win and lose games will take in the gains and losses and then reflect those changes in the database.

**Request**:

```json
[
  {
    "user_id": "integer",
    "username": "string",
    "level": "integer"
  }
]
```

**Response**:

```json
[
  {
    "success": "string"
  }
]
```

### 3.4 Log on - `/userLogin/` (POST)

Turns on a online boolean that is used for matchmaking

**Request**:

```json
[
  {
    "user_id_": "integer"
  }
]
```

**Response**:

```json
[
  {
    "success": "string"
  }
]
```

### 3.5 Log off - `/userLogout/` (POST)

Turns off a online boolean that is used for matchmaking

**Request**:

```json
[
  {
    "user_id_": "integer"
  }
]
```

**Response**:

```json
[
  {
    "success": "string"
  }
]
```

## 4. AI Help

The API calls are made that use AI to assist users:

1. `Get Recommendation`
2. `Get Insult`

### 4.1. Get Recommendation- `/recommendations/` (POST)

Generates an opponent recommendation based off information provided.

**Request**:

```json
[
  {
    "story": "string",
  }
]
```

**Response**:

```json
[
    {
        "Recommendation Response": "string"
    }
]
```

### 3.2. Get Insult - `/insult/` (POST)

Generates an insult based match results and players.

**Request**:

```json
[
  {
    "player": "string",
    "game_end_state": "string",
    "opponent": "string"
  }
]
```

**Response**:

```json
[
    {
        "Recommendation Response": "string"
    }
]
```
