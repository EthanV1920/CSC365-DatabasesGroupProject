# Performance Tuning

## Fake data modeling
[Data Construction Python File](https://github.com/EthanV1920/CSC365-DatabasesGroupProject/blob/2a7545955b9715c7d1c5b38348ee4a511d01b6f5/fake_data_gen/fake_char.py#L1)

### Table Name - Number of Rows
characters - 11 million
users - 1 million
matches - 2.2 milllion
gold_ledger - 1 million

## Performance Results
### Endpoint: Time to execute (ms)
Recommendation: 1475
Insult: 3950
Search: 183
Character Count: 179
Purchase Character: 411
New User: 248
Update User: 227
Login User: 255 
Logout User: 205
Delete User: 4050
Create Match: 1551
Join Match: 365
Update Match:202

### Slowest endpoints:
1. Purchase Character
2. Create User
3. Delete User

## Performance Tuning

1. Purchase Character
   
3. Create User
4. Delete User 



Before indexing names it was taking 80ish ms now it takes less than one
