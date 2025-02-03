from peewee import *
from .base_model import BaseModel


class Item(BaseModel):
    id = AutoField()
    type = IntegerField()
    owner = CharField(null=True)
    quantity = IntegerField()