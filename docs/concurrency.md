# Possible concurrency issues

## 1 Double User Creation

### Potential Problem

It would be possible to issue multiple requests in a way that would create duplicate usernames in the database. This phenomenon would be called a dirty read. Because our project is assuming that every username is unique, this could lead to problems when referencing users by usernames. You could have instances where one, multiple, or none of the users are referenced which would lead to game breaking problems.

### Potential Solution

A solution to this is to change the isolation level to `read committed` this would prevent dirty reads from happening altogether in the database, however, it is preferable to instead change the code to be more robust. In this case, there should be no check for a unique username but instead give ever user a unique user ID on the backend and allow any user to have any username that they want and then only refer to users by their UUID. 

```mermaid
sequenceDiagram
    autonumber
    box purple Backend
        participant d as database
        participant r as render
    end
    box blue Users
        actor a as Alice
        actor j as John
    end

    a->>+r: I would like to make a new user named Player 1
    critical
        r->>+d: Is the username Player 1 taken?
        d->>-r: No, the user name Player 1 is not taken
    end
    j->>+r: I would like to make a new user names Player 1
    critical
        r->>+d: Is the username Player 1 taken?
        d->>-r: No, the user name Player 1 is not taken
    end
    critical
        r->>+d: Make Alice Player 1
        d->>-r: Alice is now Player 1
    end
    critical
        r->>+d: Make John Player 1
        d->>-r: Alice is now Player 1
    end
    r-->>+a: You are now player 1
    r-->>+j: You are now player 1
```
