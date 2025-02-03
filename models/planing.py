from peewee import *
from .base_model import BaseModel


class Planing(BaseModel):
    id = AutoField()
    itemName = CharField()
    itemDescription = CharField()
    itemQuantity = IntegerField()
    supplier = CharField()
    price = IntegerField()
    completed = BooleanField(default=False)


