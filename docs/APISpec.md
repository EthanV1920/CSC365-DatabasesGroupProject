# API Specification for Fighting Game Backend

## 1. Shop Purchase

The API calls are made in this sequence when making a purchase:
1. `Get Inventory`
2. `Make Purchase`
3. `New Cart`
4. `Add Item to Cart` (Can be called multiple times)


### 1.1. Get Inventory - `/inventory/` (GET)

Retrieves the inventory of the player to check whether they have the currency to make a purchase and to confirm that they do not have the item already.


### 1.2. Make Purchase - `/carts/completePurchase/{cart_id}` (POST)

Uses the inventory to determine if a purchase is viable and if so updates the inventory to reflect the purchase
**Request**:

```json
[
  {
    "Item": "string",
    "Inventory_id": "number",
    "cart_id": "number"
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

### 1.3. New Cart - `/carts/` (POST)

Creates a new cart for a specific customer.

**Request**:

```json
{
  "player_id": "number",
  "inventory_id": "number",
}
```

**Response**:

```json
{
    "cart_id": "string" /* This id will be used for future calls to add items and checkout */
}
``` 

### 1.4. Add Item to Cart - `/carts/{cart_id}/items/{item_sku}` (PUT)

Updates the quantity of a specific item in a cart. 

**Request**:

```json
{
  "item_id": "number"
}
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

### 2.1. Start Match - `/match/start` (POST)

Runs an algrithm to match you up with a properly skilled opponent
**Response**:

```json
[
    {
        "Match_id": "number",
        "Oponnent_id": "number"
    }
]
```

### 2.2. End Match - `/match/end/{match_id}` (POST)

Ends the match updating data, achievements, scores, levels, etc 

**Response**

```json
[
    {
        "Success": "Boolean",
    }
]
```

## 3. Account Handling

The API calls are made that manage account activities:
1. `New Account`
2. `Delete Account`

### 3.1. New Account - `/account/new` (POST)

Gets the plan for purchasing wholesale barrels. The call passes in a catalog of available barrels
and the shop returns back which barrels they'd like to purchase and how many.

**Request**:

```json
[
  {
    "username": "string",
    "region": "string"
  }
]
```

**Response**:

```json
[
    {
        "user_id": "number"
    }
]
```

### 3.2. Delete account - `/acount/delete/{user_id}` (POST)

Deletes the entire account from the database

**Request**:

```json
[
  {
    "Success": "boolean"
  }
]
```

