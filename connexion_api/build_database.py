from config import app, db
from models import User

USERS = [
    {
        "username": "myemail@email.com",
        "password": "superSecretPass",
        "fname": "Chamoy",
        "mname": "Ray",
        "lname": "Douglas",
    },
    {
        "username": "youremail@email.com",
        "password": "1234pass",
        "fname": "Lucia",
        "mname": "",
        "lname": "Lu",
    },
]

with app.app_context():
    db.drop_all()
    db.create_all()
    for data in USERS:
        new_person = User(**data)
        #new_person = User(username=data.get("username"), password=data.get("password"), fname=data.get("fname"), mname=data.get("mname"), lname=data.get("lname"))
        db.session.add(new_person)
    db.session.commit()