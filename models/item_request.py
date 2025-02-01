from peewee import *
from .database import BaseModel


class ItemRequest(BaseModel):
    id = AutoField()
    itemId = IntegerField(null=True)
    itemName = CharField()
    itemDescription = CharField()
    itemQuantity = IntegerField()
    owner = CharField()
    status = CharField(default="Ожидает ответа")


def createItemRequest(itemId, itemName, itemDescription, itemQuantity, owner):
    ItemRequest.create(itemId = itemId, itemName = itemName, itemDescription = itemDescription, itemQuantity = itemQuantity, owner = owner)


def getItemsRequests(owner):
    if owner == None:
        itemsRequests = ItemRequest.select()
    else:
        itemsRequests = ItemRequest.select().where(ItemRequest.owner == owner)
    requests = []
    for itemRequest in itemsRequests:
        requests.append({
            'itemId': itemRequest.itemId,
            'itemName': itemRequest.itemName,
            'itemDescription': itemRequest.itemDescription,
            'itemQuantity': itemRequest.itemQuantity,
            'owner': itemRequest.owner,
            'status': itemRequest.status
        })
    return requests


if not ItemRequest.table_exists():
    ItemRequest.create_table()
    print("Table 'ItemsRequest' created")

