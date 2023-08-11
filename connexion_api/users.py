from models import User, users_schema

def get_all():
    users = User.query.all()
    return users_schema.dump(users)