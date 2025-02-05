from peewee import *
from .base_model import BaseModel
from datetime import datetime


class Report(BaseModel):
    id = AutoField()
    operationType = CharField()
    text = CharField()
    date = DateField(default=datetime.now())