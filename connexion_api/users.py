from models import User, user_schema, users_schema

def get_all(*args, **kwargs):
    users = User.query.all()
    return users_schema.dump(users)

def get_all2():
    return get_all()

def get(username: str): 
    user = User.query.filter(User.username==username).one_or_none()
    # endpoint role-based access can be added through the 
    # endpoint implementation. Downside of that approach, however,
    # is that the endpoint role is hard-coded into the implementation,
    # instead of being reflected on the openAPI specification. i.e.
    #if user.scope < admin:
    #    return None
    return user_schema.dump(user)