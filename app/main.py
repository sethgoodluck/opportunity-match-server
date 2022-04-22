import uuid
from fastapi import FastAPI

from app.api import api

description = """
This is a simple webserver that allows us to return matches on users and organizations using Levenshtein Distance to fuzzy match user interests against opportunities.
Please note that the data loaded is stored locally on the server and not connected to a persistent data store, so restarting the server will clear any loaded data.

More information is available in the README.md file

Created by Seth Martin
"""

tags_metadata = [
    {
        "name": "matches",
        "description": "Allows you to get matches and do paging as needed or filtering",
    },
    {
        "name": "opportunities",
        "description": "Add or view opportunities and keywords",
    },
     {
        "name": "users",
        "description": "You can add users and view users",
    },
    {
        "name": "organizations",
        "description": "You can view all of the organizations",
    },
    {
        "name": "server",
        "description": "Checks server status",
    },
]

app = FastAPI(
    title="Opportunity Match Server",
    description=description,
    version="0.0.1",
    openapi_tags = tags_metadata,
)

serverID = uuid.uuid4()

def _paginate(data, page_num, page_size):
    '''Helper to create pagination resp'''
    data_length = len(data)
    start = (page_num - 1) * page_size
    end = start + page_size

    resp = {
        "data": data[start:end],
        "total": len(data),
        "count": page_size,
        "pagination": {}
    }

    if end >= data_length:
        resp["pagination"]["next"] = None

        if page_num > 1:
            resp["pagination"]["previous"] = f"/matches?page_num={page_num-1}&page_size={page_size}"
        else: 
            resp["pagination"]["previous"] = None 
    else: 
        if page_num > 1:
            resp["pagination"]["previous"] = f"/matches?page_num={page_num-1}&page_size={page_size}"
        else:
            resp["pagination"]["previous"] = None

        resp["pagination"]["next"] = f"/matches?page_num={page_num+1}&page_size={page_size}"

    return resp


# ROOT / HEARTBEAT ENDPOINT
@app.get("/", tags=["server"])
def check_server():
    # Root method that just returns a heartbeat
    return {"message": "Fast API Server", "server_id": serverID}

# MATCHES ENDPOINTS
@app.get("/matches", tags=["matches"])
async def get_matches(page_num: int = 1, page_size: int = 10):
    data = api.get_all_matches()
    resp = _paginate(data, page_num, page_size)

    return resp

@app.get("/matches/org/{org_name}", tags=["matches"])
async def get_matches_by_org(org_name: str, page_num: int = 1, page_size: int = 10):
    data = api.get_all_matches(filter_by_org_name=org_name)
    resp = _paginate(data, page_num, page_size)

    return resp

@app.get("/matches/user/{user_id}", tags=["matches"])
async def get_matches_by_user(user_id: str, page_num: int = 1, page_size: int = 10):
    data = api.get_all_matches(filter_by_user_id=user_id)
    resp = _paginate(data, page_num, page_size)

    return resp

# OPPORTUNITY ENDPOINTS
@app.post("/opportunities", tags=["opportunities"])
async def add_opportunities(oppList: list):
    # Adds new opportunities
    # Expects a list of opportunity objects
    records_added = api.add_opportunities(oppList)

    return {"opportunities created": records_added}

@app.get("/opportunities", tags=["opportunities"])
async def get_opportunities(page_num: int = 1, page_size: int = 10):
    data = [*api.get_all_opportunities().values()]
    resp = _paginate(data, page_num, page_size)
    return resp

@app.get("/keywords", tags=["opportunities"])
async def get_keywords(page_num: int = 1, page_size: int = 10):
    data = [*api.get_all_keywords().values()]
    resp = _paginate(data, page_num, page_size)
    return resp

# USER ENDPOINTS
@app.post("/users", tags=["users"])
# Adds new users
# Expects a list of user objects
async def add_users(userList: list):
    users_added = api.add_users(userList)
    return {"users added": users_added}

@app.get("/users", tags=["users"])
async def get_users(page_num: int = 1, page_size: int = 10):
    data = [*api.get_all_users().values()]
    resp = _paginate(data, page_num, page_size)
    return resp

# ORG ENDPOINTS
@app.get("/orgs", tags=["organizations"])
async def get_orgs(page_num: int = 1, page_size: int = 10):
    data = [*api.get_all_orgs()]
    resp = _paginate(data, page_num, page_size)
    return resp