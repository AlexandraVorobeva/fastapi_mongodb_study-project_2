from mongoengine import Document, StringField, IntField, ListField
from pydantic import BaseModel


class Employee(Document):
    emp_id = IntField()
    name = StringField(max_length=100)
    age = IntField()
    team = ListField()


class User(Document):
    username = StringField()
    password = StringField()


class NewEmployee(BaseModel):
    emp_id: int
    name: str
    age: int
    team: list


class NewUser(BaseModel):
    username: str
    password: str