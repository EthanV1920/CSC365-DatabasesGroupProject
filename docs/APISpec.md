# API Specification for Potion Exchange Compatible Shops

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

Ends the match updating data, achievements, scores, etc 

**Response**

```json
[
    {
        "Success": "Boolean",
    }
]
```

## 3. Account Handling

The API calls are made that manage:
1. `Get Barrel Purchase Plan`
2. `Deliver Barrels`

### 3.1. Get Barrel Purchase Plan - `/barrels/plan` (POST)

Gets the plan for purchasing wholesale barrels. The call passes in a catalog of available barrels
and the shop returns back which barrels they'd like to purchase and how many.

**Request**:

```json
[
  {
    "sku": "string",
    "ml_per_barrel": "integer",
    "potion_type": "integer",
    "price": "integer",
    "quantity": "integer"
  }
]
```

**Response**:

```json
[
    {
        "sku": "string", /* Must match a sku from the catalog just passed in this call */
        "quantity": "integer" /* A number between 1 and the quantity available for sale */
    }
]
```

### 3.2. Deliver Barrels - `/barrels/deliver/{order_id}` (POST)

Posts delivery of barrels. order_id is a unique value representing
a single delivery.

**Request**:

```json
[
  {
    "sku": "string",
    "ml_per_barrel": "integer",
    "potion_type": "integer",
    "price": "integer",
    "quantity": "integer"
  }
]
```

### 4. Admin Functions

### 4.1. Reset Shop - `/admin/reset` (POST)

A call to reset shop will delete all inventory and in-flight carts and reset gold back to 100. The
shop should take this as an opportunity to remove all of their inventory and set their gold back to
100 as well.

### 5. Info Functions

### .1. Current time - `/info/current_time` (POST)

Shares what the latest time (in game time) is. 

**Request**:

```json
[
  {
    "day": "string",
    "hour": "number"
  }
]
```

### 6. Audit Functions

### 6.1. Get Inventory Summary - `/inventory/audit` (GET)

Return a summary of your current number of potions, ml, and gold.

**Response**:
```json
{
  "number_of_potions": "number",
  "ml_in_barrels": "number",
  "gold": "number"
)
```  

### 6.2 Get capacity purchase plan - `/inventory/plan` (POST)

What additional potion or ML capacity the shop would like to buy. Called once a day.
You start with 1 capacity of potion and 1 capacity of ml storage. Each potion capacity
allows 50 potion storage. Each ml capacity allows 10k of ml storage.

**Response**:
```json
{
  "potion_capacity": "number",
  "ml_capacity": "number"
}
```

### 6.3 Deliver capacity purchased - `/inventory/deliver` (POST)

Delivers capacity purchased back to shop. Called when a capacity purchase succeeds.

**Request**:
```json
{
  "potion_capacity": "number",
  "ml_capacity": "number"
}
```
