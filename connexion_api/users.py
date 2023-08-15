from models import User, user_schema, users_schema

def get_all(*args, **kwargs):
    users = User.query.all()
    return users_schema.dump(users)

def get_all2():
    return get_all()

def get(username: str):
    user = User.query.filter(User.username==username).one_or_none()
    return user_schema.dump(user)