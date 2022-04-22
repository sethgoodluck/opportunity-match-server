import uuid 
from app.db import MockDB
from thefuzz import process

db = MockDB.db

def get_all_opportunities():
    return [*b['opps'].items()]

def get_all_users():
    return [*db['users'].items()]

def get_all_orgs():
    return [*db['orgs'].items()]

def get_all_keywords():
    return [*db['matches'].items()]

def _add_org(org: str) -> None:
    '''Helper checks if org exists, adds it if it does not'''

    if org not in db['orgs']:
        db['orgs'][org] = {
                'org_id': uuid.uuid4() , 
                'opps': []
            }

def _add_keyword(keyword: str) -> bool:
    '''Adds keyword if it does not exist
    Returns a boolean for whether the keyword was added
    If the keyword was added, matches need to be refreshed
    '''

    if keyword not in db['matches']:
        db['matches'][keyword] = {
                'opps': {}, 
                'users': {}
            }
        
        return True
    
    return False

def _process_interests(user):
    '''Processes a user interest list against keywords using he Levenshtein Distance metric
    made available through fuzzywuzzy. When the score is greater than 60%, we consider it a match. 
    '''
    interests = user.get('interested_in', [])
    keywords = db['matches'].keys()

    for keyword in keywords:
        matches = list(process.extractWithoutOrder(keyword, interests, score_cutoff=90))

        for match in matches:
            # For the keyword, add the relevant user info
            fname = user.get('first_name','') or ''
            lname = user.get('last_name', '') or ''

            userObj = {
                'user_name': fname + ' ' + lname,
                'interest': match[0],
                'match_lvl': match[1]
            }

            db['matches'][keyword]['users'][user.get('id')] = userObj

def get_all_matches(filter_by_org_name = None, filter_by_user_id = None):
    '''For each keyword, for each opp, for each user => create match
    Append the match to a list of matches
    Return all matches 
    '''
    all_matches = []

    for key, obj in db['matches'].items():
        for oppId, orgName in obj['opps'].items():
            
            if filter_by_org_name and filter_by_org_name != orgName:
                continue    # Filter non matching orgs when org name is provided
            
            for userId, userObj in obj['users'].items():

                if filter_by_user_id and filter_by_user_id != str(userId):
                    continue    # Filter non matching users when user id is provided

                match = {
                    'keyword': key,
                    'opp_id': oppId,
                    'user_id': userId,
                    'org_name': orgName,
                    'user_name': userObj.get('user_name', ''),
                    'interest': userObj.get('interest', ''),
                    'match_level': userObj.get('match_lvl', -1)
                }

                all_matches.append(match)

    return all_matches

def add_opportunities(opportunityList: list[str]):
    '''Adds opportunities to the opps db
    Updates the orgs db 
    Updates the matches db 

    Expects a list of opportunities 
    Updates relevant DBs 
    '''

    for opp in opportunityList:
        org = opp.get('organization', '')
        email = opp.get('email', 'No Email Available')

        _add_org(org)   # Add the org if it does not exist 

        for role in opp.get('roles', []):
            
            refresh = _add_keyword(role)

            oppId = str(uuid.uuid4())        # Create a unique opp ID (handled by DBs typically)            
            
            newOpp = {
                'id': oppId, 
                'role': role, 
                'email': email, 
                'org': org
                }

            db['opps'][oppId] = newOpp     # Add the opp object to our opps collection
            db['orgs'][org]['opps'].append(oppId)
            db['matches'][role]['opps'][oppId] = org

    return len(opportunityList)

def add_users(userList):
    '''Adds users to the users DB
    Fuzzy Matches on interests keywords
    '''
    for user in userList:
        db['users'][user.get('id')] = user 

        _process_interests(user)
    
    return len(userList)