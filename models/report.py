from peewee import *
from .base_model import BaseModel
from datetime import datetime


class Report(BaseModel):
    id = AutoField()
    text = CharField()
    date = DateField(default=datetime.now())