from peewee import *
from .base_model import BaseModel


class ItemType(BaseModel):
    type = AutoField()
    name = CharField()
    description = CharField(null = True)
    status = CharField(default = "Новый")
