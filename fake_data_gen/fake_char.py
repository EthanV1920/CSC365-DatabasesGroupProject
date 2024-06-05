from faker import Faker
import sqlalchemy
import database as db
import random
from sqlalchemy import text
import csv


fake = Faker()

# user generation
# for _ in range(7):
#     result = ""
#     fake = Faker(['it_IT', 'en_US', 'de_DE', 'fr_FR', 'es_ES', 'nl_NL', 'pt_PT'])
#     for _ in range(100000):
#         name = fake.name().replace("'", "")  # removes single quotes
#         level = fake.random_int(min=1, max=100)
#         result += "INSERT INTO users (username, level) VALUES ('" +  name + "' , " + str(level) + ");"

#     with db.engine.begin() as connection:
#         sqltxt = sqlalchemy.text(result)
#         connection.execute(sqltxt)
#     print(result)

# #Char inventory generation 1001131
# fake = Faker(['en_US'])
# params = []

# # Fetch valid user IDs from the database
# with db.engine.begin() as connection:
#     result = connection.execute(text("""
#         SELECT user_id FROM users
#     """))
#     valid_user_ids = [row[0] for row in result]

# # Open a CSV file for writing
# with open('characters_ledger.csv', 'w', newline='') as csvfile:
#     fieldnames = ['user_id', 'character_id']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     # Write the header
#     writer.writeheader()

#     # Loop over valid user IDs
#     for user_id in valid_user_ids:
#         chars = []
#         for _ in range(10):
#             char_id = fake.random_int(min=38, max=74)
#             if char_id not in chars:
#                 chars.append(char_id)
#                 params.append({"user_id": user_id, "character_id": char_id})

#         # Write the rows to the CSV file in batches of 10000
#         if len(params) >= 10000:
#             writer.writerows(params)
#             print("wrote 10000")
#             params = []

#     # Write any remaining rows to the CSV file
#     if params:
#         writer.writerows(params)


# Gold ledger generation
fake = Faker(['en_US'])
params = []

# Fetch valid user IDs from the database
with db.engine.begin() as connection:
    result = connection.execute(text("""
        SELECT user_id FROM users
    """))
    valid_user_ids = [row[0] for row in result]

# Open a CSV file for writing
with open('gold_ledger.csv', 'w', newline='') as csvfile:
    fieldnames = ['user_id', 'gold']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Loop over valid user IDs
    for user_id in valid_user_ids:
        gold = int((random.random() ** 2) * (125000 - 50) + 50)
        params.append({"user_id": user_id, "gold": gold})

        # Write the rows to the CSV file in batches of 10000
        if len(params) >= 10000:
            writer.writerows(params)
            print("wrote 10000")
            params = []

    # Write any remaining rows to the CSV file
    if params:
        writer.writerows(params)


#match generation
# for _ in range(10):
#     result = ""
#     wincount = 0
#     losscount = 0
#     tiecount = 0
#     fake = Faker(['en_US'])
#     for _ in range(100000):
#         player = fake.random_int(min=1, max=1001131)
#         opponent = fake.random_int(min=1, max=1001131)
#         while player == opponent:
#             opponent = fake.random_int(min=1, max=1001131)
#         weights = [45, 45, 10]  # weights for 1, 2, and 3
#         status = random.choices([1, 2, 3], weights=weights, k=1)[0]
#         if status == 1:
#             wincount += 1
#         elif status == 2:
#             losscount += 1
#         else:
#             tiecount += 1
#         player_char1 = fake.random_int(min=38, max=74)
#         player_char2 = fake.random_int(min=38, max=74)
#         result += "INSERT INTO matches (player1, player2, status, player_char1, player_char2) VALUES (" + str(player) + " , " + str(opponent) + " , '" + str(status) + "' , " + str(player_char1) + " , " + str(player_char2) +");"
#     # with db.engine.begin() as connection:
#     #     sqltxt = sqlalchemy.text(result)
#     #     connection.execute(sqltxt)
#     print(result)
#     print(str(wincount) + " " + str(losscount) + " " + str(tiecount))


