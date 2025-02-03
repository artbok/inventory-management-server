from peewee import *
from .base_model import BaseModel


class ReplacementRequest(BaseModel):
    id = AutoField()
    owner = CharField()
    itemId = IntegerField()
    quantity = IntegerField()
    status = CharField(default='created')


