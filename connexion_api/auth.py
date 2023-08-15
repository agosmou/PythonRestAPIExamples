from users import User
from flask import request, redirect

def verifyUserPass(username, password, required_scopes):
    ## required_scopes always None!
    user = User.query.filter(User.username==username).one_or_none()
    if user and user.password == password:
        return {
            "scope": "read write"
        }
    return None

def verifyToken(token_string, required_scopes):
    '''
    At a minimum this function should return
    the authenticated scope for token_string. 
    In practice, however, we should return a dict
    that complies with RFC 7662
    https://datatracker.ietf.org/doc/html/rfc7662
    '''
    ## required_scopes always None!
    if token_string == "read-token":
        return {
            "scope": ["read"]
        }
    elif token_string == "write-token":
        return {
            "scope": "read write"
        }
    else:
        return None