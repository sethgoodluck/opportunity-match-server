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