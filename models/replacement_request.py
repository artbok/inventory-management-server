from peewee import *
from .database import BaseModel
from .item import getItem
from .item_owner import getItemOwner


class ReplacementRequest(BaseModel):
    id = AutoField()
    owner = CharField()
    itemId = IntegerField()
    itemName = CharField()
    itemDescription = CharField(null=True)
    itemQuantity = IntegerField()
    status = CharField(default='created')


def createReplacementRequest(owner, itemId, quantity):
    item = getItem(itemId)
    item.quantity -= quantity
    item.save()
    request: ReplacementRequest = ReplacementRequest.get_or_none(ReplacementRequest.itemId == itemId, ReplacementRequest.owner == owner, ReplacementRequest.status == "created")
    if request:
        request.itemQuantity += quantity
        request.save()
    else:
        ReplacementRequest.create(owner = owner, itemId = itemId, itemName = item.name, itemDescription = item.description, itemQuantity = quantity)
    itemOwner = getItemOwner(owner, itemId)
    itemOwner.itemQuantity -= quantity
    itemOwner.save()
    if itemOwner.itemQuantity == 0:
        itemOwner.delete_instance()
    if item.quantity == 0:
        item.delete_instance()


def getReplacementsRequests(owner):
    items = []
    if owner == None:
        requests = ReplacementRequest.select()
    else:
        requests = ReplacementRequest.select().where(ReplacementRequest.owner == owner)
    
    for replacementRequest in requests:
        items.append({
            'itemName': replacementRequest.itemName,
            'description': replacementRequest.itemDescription,
            'quantity': replacementRequest.itemQuantity,
            'status': replacementRequest.status 
        })
    return items


if not ReplacementRequest.table_exists():
    ReplacementRequest.create_table()
    print("Table 'ReplacementRequest' created")
