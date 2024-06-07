# Performance Tuning

## Fake data modeling
[Data Construction Python File](https://github.com/EthanV1920/CSC365-DatabasesGroupProject/blob/2a7545955b9715c7d1c5b38348ee4a511d01b6f5/fake_data_gen/fake_char.py#L1)

### Table Name - Number of Rows
characters - 11 million<br />
users - 1 million<br />
matches - 2.2 milllion<br />
gold_ledger - 1 million<br />

## Performance Results
### Endpoint: Time to execute (ms)
Recommendation: 1475<br />
Insult: 3950<br />
Search: 183<br />
Character Count: 179<br />
Purchase Character: 411<br />
New User: 248<br />
Update User: 227<br />
Login User: 255 <br />
Logout User: 205<br />
Delete User: 4050<br />
Create Match: 1551<br />
Join Match: 365<br />
Update Match: 202<br />

### Slowest endpoints:
The Recommendation and Insult endpoints take long because they're being powered by AI, therefore we cannot improve their performance through indexing. Instead, we chose to improve the performance of the other three slowest endpoints:
1. Purchase Character
2. Create User
3. Delete User

## Performance Tuning

1. Purchase Character: New Execution Time = 268 ms
3. Create Match: New Execution Time = 296 ms
4. Delete User: New Execution Time = 202 ms
<br />explain
  SELECT users.user_id, characters.character_id, COALESCE(SUM(gold_ledger.gold), 0)
  FROM users
  LEFT JOIN characters ON characters.name = 'Jade'
  LEFT JOIN gold_ledger ON users.user_id = gold_ledger.user_id
  WHERE users.username = 'Victoria'
  GROUP BY users.user_id, characters.character_id

| QUERY PLAN                                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------------- |
| GroupAggregate  (cost=10.56..10.60 rows=2 width=16) (actual time=0.085..0.086 rows=1 loops=1)                                                     |
|   Group Key: users.user_id, characters.character_id                                                                                               |
|   ->  Sort  (cost=10.56..10.57 rows=2 width=12) (actual time=0.080..0.081 rows=4 loops=1)                                                         |
|         Sort Key: users.user_id, characters.character_id                                                                                          |
|         Sort Method: quicksort  Memory: 25kB                                                                                                      |
|         ->  Nested Loop Left Join  (cost=0.85..10.55 rows=2 width=12) (actual time=0.049..0.056 rows=4 loops=1)                                   |
|               ->  Nested Loop Left Join  (cost=0.85..9.06 rows=2 width=8) (actual time=0.032..0.036 rows=4 loops=1)                               |
|                     ->  Index Scan using users_full_name_idx on users  (cost=0.42..3.76 rows=2 width=4) (actual time=0.023..0.023 rows=1 loops=1) |
|                           Index Cond: (username = 'Ethan'::text)                                                                                  |
|                     ->  Index Scan using gold_id_index on gold_ledger  (cost=0.42..2.64 rows=1 width=8) (actual time=0.007..0.010 rows=4 loops=1) |
|                           Index Cond: (user_id = users.user_id)                                                                                   |
|               ->  Materialize  (cost=0.00..1.47 rows=1 width=4) (actual time=0.004..0.004 rows=1 loops=4)                                         |
|                     ->  Seq Scan on characters  (cost=0.00..1.46 rows=1 width=4) (actual time=0.012..0.014 rows=1 loops=1)                        |
|                           Filter: (name = 'Jade'::text)                                                                                           |
|                           Rows Removed by Filter: 36                                                                                              |
| Planning Time: 1.835 ms                                                                                                                           |
| Execution Time: 0.182 ms                                                                                                                          |

Based off the above query plan, we decided to index the user_id in gold_ledger to avoid that sequential search. The other sequential search in the query plan is on the characters table, but we chose not to index this because the tablewill always be only 30 rows long and indexing would not create a significant change in performance:

create index gold_user_index ON gold_ledger (user_id)

| QUERY PLAN                                                                                                                                          |
| --------------------------------------------------------------------------------------------------------------------------------------------------- |
| GroupAggregate  (cost=10.56..10.60 rows=2 width=16) (actual time=0.094..0.095 rows=1 loops=1)                                                       |
|   Group Key: users.user_id, characters.character_id                                                                                                 |
|   ->  Sort  (cost=10.56..10.57 rows=2 width=12) (actual time=0.088..0.090 rows=4 loops=1)                                                           |
|         Sort Key: users.user_id, characters.character_id                                                                                            |
|         Sort Method: quicksort  Memory: 25kB                                                                                                        |
|         ->  Nested Loop Left Join  (cost=0.85..10.55 rows=2 width=12) (actual time=0.057..0.065 rows=4 loops=1)                                     |
|               ->  Nested Loop Left Join  (cost=0.85..9.06 rows=2 width=8) (actual time=0.040..0.044 rows=4 loops=1)                                 |
|                     ->  Index Scan using users_full_name_idx on users  (cost=0.42..3.76 rows=2 width=4) (actual time=0.026..0.026 rows=1 loops=1)   |
|                           Index Cond: (username = 'Ethan'::text)                                                                                    |
|                     ->  Index Scan using gold_user_index on gold_ledger  (cost=0.42..2.64 rows=1 width=8) (actual time=0.011..0.014 rows=4 loops=1) |
|                           Index Cond: (user_id = users.user_id)                                                                                     |
|               ->  Materialize  (cost=0.00..1.47 rows=1 width=4) (actual time=0.004..0.005 rows=1 loops=4)                                           |
|                     ->  Seq Scan on characters  (cost=0.00..1.46 rows=1 width=4) (actual time=0.012..0.014 rows=1 loops=1)                          |
|                           Filter: (name = 'Jade'::text)                                                                                             |
|                           Rows Removed by Filter: 36                                                                                                |
| Planning Time: 1.020 ms                                                                                                                             |
| Execution Time: 0.198 ms                                                                                                                            |
