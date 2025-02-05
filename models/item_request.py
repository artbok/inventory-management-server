from peewee import *
from .base_model import BaseModel


class ItemRequest(BaseModel):
    id = AutoField()
    type = IntegerField(null=True)
    quantity = IntegerField()
    owner = CharField()
    status = CharField(default="Ожидает ответа")

