from peewee import *
from .database import BaseModel

class Plan(BaseModel):
    id = AutoField()
    itemName = CharField()
    itemDescription = CharField()
    itemQuantity = IntegerField()
    supplier = CharField()
    price = IntegerField()
    completed = BooleanField(default=False)


if not Plan.table_exists():
    Plan.create_table()
    print("Table 'Plan' created")