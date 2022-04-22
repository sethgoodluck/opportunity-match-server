# Opportunity Match API

Coding challenge to create an API that provides matches between candidates and opportunities.

## Final State

This was a fun project but would honestly take me more than 4 hours to fully flesh out into something I would call "production ready".

Some things that I would have liked to do given more time include:

- Containerization (docker)
- Persistent Data Store (mongodb)
- Handling edge cases such as a user with no listed interests
  - they are presently ignored in the GET /matches endpoint
- Using workers to do things like upload a large set of users
  - This is a slow process right now as each user has to get parsed during upload
  - In the real world, I'd set this up in a lambda function or similar process so it can be done in the background
  - This could also be sped up substantially the faster fuzzywuzzy package 

That being said, the primary objective to allow ingesting of users and opportunities and match returns was completed. I was quite content using the fuzzy matching to give a broader chance for matching.

I left the README below untouched to allow you some sense of how I went about approaching the problem.

All the best,

Seth Martin

## How to Run

I ran out of time before containerizing the application. As such, you will need to run it as follows:

1. Spin up a virtual environment and activate it 

    ```bash
    python3 -m venv venv
    ```

    ```bash
    . venv/bin/activate
    ```

2. Install the necessary dependencies

    ```bash
    pip install -r requirements.txt
    ```

3. Run the application

    ```bash
    uvicorn app.main:app --reload
    ```

4. After the server is up, you can check and test all endpoints at the following url: [localhost:8000/docs](localhost:8000/docs)

## Shortcomings and Known Issues

1. You must upload opportunities before uploading users
   1. Uploading subsequent opportunities does not properly update match states
2. We do not return users with no matches in the get all matches call
3. Uploading all of the users at once is a slow process due to fuzzywuzzy parsing
   1. Doable on an average machine but we would want a better way to do this

## Initial Thoughts

To me, the key consideration for this problem is how we organize our data.

At a high-level, there are organizations, roles, users, and interests.
My first thought is that I want to use some kind of FuzzyMatch to match users to opportunities when the matches are approxmiate.

I'm going to parse through the data to identify any notable edge cases or patterns that will influence design.

## Questions, Notes, & Observations

- Each opportunity has its own nullable email contact
  - If a contact is null what should we do?
    - We will ignore it for now as our return object does not have the contact email

- Users can have no interests listed
  - If a user has no interests, they won't match on anything by default
    - We will return a "No matches" array of said users

- An organization can have multiple "identical" opportunities
  - We will need to make sure that each opportunity is stored uniquely

## High Level Approach

### Create high level collections schemas as follows

    ```python
        opps = {
                id: {
                    role: str,
                    email: str,
                    org: str
                }
            }
        
        orgs = {
                org_name: {
                    org_id: int
                    opps: [opp_ids],
                }
            }
        
        users = {
                user_email: {
                    user_id: int,
                    first_name: str,
                    last_name: str,
                    interests: [str]
                }
            }

        matches = {
            keyword: {
                opps: {
                    opp_id: {
                        org_name
                    }
                }
                users: {
                    user_id: {
                        user_name: str, 
                        interest: str, 
                        match_lvl: float
                    }
                }
            }
    ```

Note on "matches" collection

- We are going to keep two separate lists in each keyword document
- This keeps the store "smaller" and  makes updating matches easier in the future easier (just add or remove IDs)
- The arrays contain just what we want to return in `GET /matches` for now and give us O(1) lookups if we need additional info from other collections

The return from `GET /matches` will take the following form:

    ```json
        [
            {
                opp_id
                user_id
                keyword
                interest_name
                match_level
            }, 
            ...
        ]
    ```

    And our approximate algorithm for returning that may take this form:

    ```python
        For each keyword in matches
            For each opp in opps
                each user in users
                    return match_object 
    ```

### What happens when we add users or opportunities?

    USERS
    1. Update users
    2. Fuzzy Match their interests

    OPPORTUNITIES
    1. Update opps and orgs 
    2. If keyword exists, append opp ID else create new opp and generate matches

### Critical endpoints

I will create the following endpoints _( * = Optional, but desired. ** = Only if I have time )_

    GET /matches => Returns paged list of all matches 
    *GET /matches/{keyword} => Returns matches for specicic keyword 
    **GET /matches/organization/{org_id} => Returns matches for a specific org
    **GET /matches/user/{user_id} => Returns matches for a specific user

    POST /opportunities=>  Adds an [opportunity]
    *GET /opportunities/{id} => Returns opportunity details 
    *GET /oppportunities => Returns a list of all opportunities 
    **PUT /opportunity/{id} => Updates an opportunity

    *POST /organizations => Adds an organization
    *GET /organizations/{id} => Gets organization details 
    *GET /organizations => Returns a list of all organizations
    **PUT /organization/{id} => Updates an organization 

    POST /users => Adds a [user]
    *GET /users/{id} => Gets a user details 
    *GET /users => Returns a list of all users 
    **PUT /users/{id} => Updates a user

    **DELETE /opportunity/{id} => Removes an opportunity 
    **DELETE /organization/{id} => Removes an org and all related opportunities 
    **DELETE /user/{id} => Removes a user

### Technologies

I will use the following technologies to create this API
_* = desired but only if I have time_
  
- Python
- FuzzyWuzzy (string matching library)
- FastAPI
- *MongoDB
- *Docker
- *Heroku

### Next Steps

I believe this is a good start on this problem. While I could have just started hacking something together, I tend to enjoy thinking through what I'm doing before programming. So, I spent a good hour or so writing notes, considering the data, and coming up with a plan. Next steps are as follows. (_* = I will only do these if I have the extra time_)

- [X] Setup FastAPI Server
- [X] Scaffold Unit Tests
- [X] Scaffold Endpoints
- [X] Build out "mock" database
- [X] Build out ingestion processing functions
- [ ] *Connect MongoDB Atlas
- [ ] *Containerize via Docker
- [ ] *Deploy for live demonstration
