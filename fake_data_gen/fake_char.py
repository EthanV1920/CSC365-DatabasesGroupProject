from faker import Faker
import sqlalchemy
import database as db
import random

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


#match generation
for _ in range(10):
    result = ""
    wincount = 0
    losscount = 0
    tiecount = 0
    fake = Faker(['en_US'])
    for _ in range(100000):
        player = fake.random_int(min=1, max=1001131)
        opponent = fake.random_int(min=1, max=1001131)
        while player == opponent:
            opponent = fake.random_int(min=1, max=1001131)
        weights = [45, 45, 10]  # weights for 1, 2, and 3
        status = random.choices([1, 2, 3], weights=weights, k=1)[0]
        if status == 1:
            wincount += 1
        elif status == 2:
            losscount += 1
        else:
            tiecount += 1
        player_char1 = fake.random_int(min=38, max=74)
        player_char2 = fake.random_int(min=38, max=74)
        result += "INSERT INTO matches (player1, player2, status, player_char1, player_char2) VALUES (" + str(player) + " , " + str(opponent) + " , '" + str(status) + "' , " + str(player_char1) + " , " + str(player_char2) +");"
    # with db.engine.begin() as connection:
    #     sqltxt = sqlalchemy.text(result)
    #     connection.execute(sqltxt)
    print(result)
    print(str(wincount) + " " + str(losscount) + " " + str(tiecount))


