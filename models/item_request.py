from peewee import *
from .base_model import BaseModel


class ItemRequest(BaseModel):
    id = AutoField()
    type = IntegerField(null=True)
    itemName = CharField(null=True)
    itemDescription = CharField(null=True)
    itemQuantity = IntegerField()
    owner = CharField()
    status = CharField(default="Ожидает ответа")

