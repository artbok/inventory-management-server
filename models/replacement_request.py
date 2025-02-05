from peewee import *
from .base_model import BaseModel


class ReplacementRequest(BaseModel):
    id = AutoField()
    owner = CharField()
    type = IntegerField()
    quantity = IntegerField()
    status = CharField(default="Ожидает ответа")


