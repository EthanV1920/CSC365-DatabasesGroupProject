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
2. Create Match: New Execution Time = 296 ms
<br />explain
  with user_level as (select level
                    from users
                    where user_id = :user_id),
     opponent
         as (select nullif(user_id, (select player2 from matches where player2 = :user_id and player2_char is null)) as user_id
             from users,
                  user_level
             where users.level between user_level.level - 5 and user_level.level + 5
               and user_id != :user_id
               and (select online
                    from users
                    where user_id = :user_id) = true
               and online = true
             order by random()
             limit 1)
insert into
  matches (
    player1,
    player1_char,
    player2,
    player2_char,
    status
  )
values
  (
    :user_id,
    :user_char,
    (
      select
        *
      from
        opponent
    ),
    null,
    -1
  )
returning
  id,
  player2;

| QUERY PLAN                                                                                                                   |
| ---------------------------------------------------------------------------------------------------------------------------- |
| Insert on matches  (cost=71139.32..71139.34 rows=1 width=48)                                                                 |
|   CTE opponent                                                                                                               |
|     ->  Limit  (cost=71139.30..71139.30 rows=1 width=12)                                                                     |
|           InitPlan 1 (returns $0)                                                                                            |
|             ->  Seq Scan on matches matches_1  (cost=0.00..49574.98 rows=1 width=8)                                          |
|                   Filter: ((player2_char IS NULL) AND (player2 = 12345))                                                     |
|           InitPlan 2 (returns $1)                                                                                            |
|             ->  Index Scan using user_id_index on users  (cost=0.42..2.64 rows=1 width=1)                                    |
|                   Index Cond: (user_id = 123456)                                                                             |
|           ->  Sort  (cost=21561.68..21561.68 rows=1 width=12)                                                                |
|                 Sort Key: (random())                                                                                         |
|                 ->  Result  (cost=0.42..21561.67 rows=1 width=12)                                                            |
|                       One-Time Filter: $1                                                                                    |
|                       ->  Nested Loop  (cost=0.42..21561.66 rows=1 width=4)                                                  |
|                             Join Filter: ((users_1.level >= (users_2.level - 5)) AND (users_1.level <= (users_2.level + 5))) |
|                             ->  Seq Scan on users users_1  (cost=0.00..21559.00 rows=1 width=8)                              |
|                                   Filter: (online AND (user_id <> 123456))                                                   |
|                             ->  Index Scan using user_id_index on users users_2  (cost=0.42..2.64 rows=1 width=4)            |
|                                   Index Cond: (user_id = 123456)                                                             |
|   InitPlan 4 (returns $3)                                                                                                    |
|     ->  CTE Scan on opponent  (cost=0.00..0.02 rows=1 width=4)                                                               |
|   ->  Result  (cost=0.00..0.02 rows=1 width=48)                                                                              

Based off the above query plan, we decided to index the player1 and player2 in matches as well as online in users

create index player1_index ON matches (player1)
create index player2_index ON matches (player2)
create index online_index ON users (online)

| QUERY PLAN                                                                                                                        |
| --------------------------------------------------------------------------------------------------------------------------------- |
| Insert on matches  (cost=12.89..12.91 rows=1 width=48) (actual time=2.205..2.208 rows=1 loops=1)                                  |
|   CTE opponent                                                                                                                    |
|     ->  Limit  (cost=12.86..12.87 rows=1 width=12) (actual time=0.060..0.061 rows=0 loops=1)                                      |
|           InitPlan 1 (returns $0)                                                                                                 |
|             ->  Index Scan using player2_index on matches matches_1  (cost=0.43..6.00 rows=1 width=8) (never executed)            |
|                   Index Cond: (player2 = 12345)                                                                                   |
|                   Filter: (player2_char IS NULL)                                                                                  |
|           InitPlan 2 (returns $1)                                                                                                 |
|             ->  Index Scan using users_pkey on users  (cost=0.42..2.64 rows=1 width=1) (actual time=0.036..0.037 rows=1 loops=1)  |
|                   Index Cond: (user_id = 123456)                                                                                  |
|           ->  Sort  (cost=4.22..4.23 rows=1 width=12) (actual time=0.059..0.059 rows=0 loops=1)                                   |
|                 Sort Key: (random())                                                                                              |
|                 Sort Method: quicksort  Memory: 25kB                                                                              |
|                 ->  Result  (cost=0.85..4.21 rows=1 width=12) (actual time=0.039..0.039 rows=0 loops=1)                           |
|                       One-Time Filter: $1                                                                                         |
|                       ->  Nested Loop  (cost=0.85..4.21 rows=1 width=4) (never executed)                                          |
|                             Join Filter: ((users_1.level >= (users_2.level - 5)) AND (users_1.level <= (users_2.level + 5)))      |
|                             ->  Index Scan using online_index on users users_1  (cost=0.42..1.55 rows=1 width=8) (never executed) |
|                                   Index Cond: (online = true)                                                                     |
|                                   Filter: (user_id <> 123456)                                                                     |
|                             ->  Index Scan using users_pkey on users users_2  (cost=0.42..2.64 rows=1 width=4) (never executed)   |
|                                   Index Cond: (user_id = 123456)                                                                  |
|   InitPlan 4 (returns $3)                                                                                                         |
|     ->  CTE Scan on opponent  (cost=0.00..0.02 rows=1 width=4) (actual time=0.061..0.061 rows=0 loops=1)                          |
|   ->  Result  (cost=0.00..0.02 rows=1 width=48) (actual time=0.699..0.700 rows=1 loops=1)                                         |
| Planning Time: 3.828 ms                                                                                                           |
| Execution Time: 2.345 ms   

3. Delete User: New Execution Time = 202 ms
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
