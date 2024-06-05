#Code Review Response:

##Sofia Bryukhova
1. Fixed potential sql injection
2. MATCH PROBLEM
3. MATCH PROBLEM
4. Rather not introduce a more complicated sql statement for a low priority issue currently
5. Every shop item is locked at 100 gold for reduced complexity of the system, thus we should be good for now, should we wish to make the shop more complicated we will later
6. Fixed sql injection
7. Not positive what you mean by this
8. Agreed, consolidated sql calls
9. Agreed, fixed
10. Cosmetic/style changes are lower on our priorities currently
11. Default Level is 1 since every account starts at level 1 no need to change that
12. Agreed we are working on fixing our style
13. Yeah we’ll start removing useless comments

##Dre Suguitan
1. ‘sqlalchemy.text()’ added to connection.execute command in users.py
****2. usersNew errors out when username is not found in database, but that is what is supposed to happen when adding the username. Replace with IntegrityError (see schema comments about making username a unique attribute)
3. ‘name’ changed to ‘username’ in users.py methods
**** 4. users.py methods error out with different json formats than when they run correctly (I don’t know if this will affect anything)
5. dbstats changes to new_user
6. Kept fetchone() instead of scalar_one() where fitting, when grabbing non scalar values.
7. Added userLogin and userLogout check for user’s status beforehand to catch any stray cases where an API call tries to log in a user already online (or the opposite)
8. Not added yet but good idea for future development
9. Not yet added due to sql injection concerns
10. CartCheckout BaseModel is being used
****11. add_to_cart querying for userId may be redundant. See schema comments about removing user_id from cart_items.
****12. A view of sum(gold) could be made so that the aggregate function did not have to be ran every charPurchase API called.

##Ethan Swenke
1. traits no longer aliased in search endpoint, for readability
****2. I'm not sure what the purpose of the dbstats endpoint is currently in characters. I would suggest some more logic to retrieve stats on wins, losses, traits, etc.
3. In match, for the duplicate dbstats function the actual route and function name seems to be copy pasted from user/character function name changed from dbstats to new_user
****4. The way match_end is set up, the winner is passed in as a string. Does this mean the winner is selected by the user? I feel like an improvement would be to have this be random, or add some logic that creates a percentage of winning chance based on the delta between two characters stats, and then choose the winner that way
5. 'scalar()' changed to ‘scalar_one()’ in the create_cart endpoint to ensure only one id gets returned and not more than 1
6. CartCheckout class removed
****7. I briefly touched on this in the API/Scheme improvements, but the checkout boolean isn't really necessary
****8. I couldn't find a place in which a user gains gold, only where they can spend it. Might I add a functionality to winning a match that adds gold to the user's inventory/ledger?
9. May be, but seems necessarily complex since selecting from different tables under different conditions
10. Should be ‘username’ and is fixed now
11. Proper check for already existing username when creating user added
12. Same as above for user deletion
****13. Why are we choosing how to update the user's level? I feel there should be some logic on the backend that decides when and how to update the user's level.


#Schema/API Design Comments

##Sofia Bryukhova
1. True, fixed
2. We have started adding indices
3. Our integers are smaller numbers that will never need to be bigint
4. We don't exactly have unique use cases that would require it but we will keep the consideration in mind
5. We felt that the character table was a fair bit bloated for all it had, we wanted to make the character table small so should we wish to add more, ie a table for assets, a table for lore, etc we wouldn't make it unreadable
6. Don't know how we forgot xp, nice catch
7. Currently the only items in the shop are characters, unfortunately our eyes were a bit big when we began
8. Generally everything is run server side
9. We are now in the process of populating tables with data
10. Carts does that
11. That is managed in the shop

##Dre Suguitan
1. Python script for pre populating table added
****2. cart_items table doesn’t necessarily need line_item_id as cart_id and character_id can be a composite key
3. User_id removed from cart items
4. Characters have multiple traits
5. Handled in the endpoint definition
6. Not in use right now but good for consideration
****8. Start Match doesn’t need “Winner” in request or “match_id” in response.
9. Start Match parameter changed to user_id
10. “Success” type based of information given to user at return
11. Great idea, we we’re not able to implement this yet but definitely needed for future stage
12. Should be fixed so all valid cart items can be checked out


##Ethan Swenke
****1. I would remove the 'winner' field from the request for start match... I'm not sure why that is needed in starting the match
2. Yes, this was updated
3. Doing this here as a response for user experience and ease of use
4. It updates the users level
5. Yes it’s helpful when just iterating through transactions
6. Yes, fixed
7. Depends on if used in the table or not
8. Could be a creative idea for future development but unnecessary in this stage
9. It would be slightly more convenient but less user friendly, as the user_id is randomly generated by the database while username is set by the user
10. Python script for populating table added
11. Helpful for not checking out orders more than once
12. Notes and user_id removed from cart_items table

#Test Result
We had two major errors at the time of the code review, the biggest being that many of our endpoints contained bugs causing Internal Server Errors. Additionally, we slightly changed the scope and trajectory of our project, so the workflows are no longer relevant to how we are currently using our database. However, we’ve tested similar workflows, tailored to our new use cases and the endpoints appear to be working as intended without server errors.

#Product Ideas

##Sofia Bryukhova
1. We are doing a complete revamp of our match system currently, it is one of our weakest points currently
2. We actually now have an endpoint to recommend characters to users based on anything really

##Dre Suguitan
1. Yes, this is something we plan to add if time allows, however for the time being we decided to focus or project and database around characters
2. I love this idea, it would be great to add when we expand past a character focused database.

##Ethan Swenke
1. Great idea, adding complexity to t=matches to reflect actual gameplay and events is one of the next goals for us.
2. This is a good idea, and we were intending on adding this functionality but decided to center our project around characters, making the scope and plans more realistic and adding complexity where possible and time allows.
