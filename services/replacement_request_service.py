from peewee import *
from models.replacement_request import ReplacementRequest
from services.item_type_service import getItemType, createItemType
from services.item_service import createItem, Item


def createReplacementRequest(owner, itemId, quantity):
    item: Item = Item.get_by_id(itemId)
    item.quantity -= quantity
    item.save()
    
    itemType = getItemType(item.type)
    newItemType = createItemType(itemType.name, itemType.description, "Сломанный")
    if item.quantity == 0:
        item.delete_instance()
    item = createItem(owner, newItemType.type, quantity)
    
    request: ReplacementRequest = ReplacementRequest.get_or_none(ReplacementRequest.itemId == item.id, ReplacementRequest.owner == owner, ReplacementRequest.status == "created")
    if request:
        request.quantity += quantity
        request.save()
    else:
        ReplacementRequest.create(owner = owner, itemId = item.id, quantity = quantity)
    


def getReplacementsRequests(owner):
    items = []
    if owner == None:
        requests = ReplacementRequest.select()
    else:
        requests = ReplacementRequest.select().where(ReplacementRequest.owner == owner)
    
    for replacementRequest in requests:
        item: Item = Item.get_by_id(replacementRequest.itemId)
        itemType = getItemType(item.type)
        items.append({
            'name': itemType.name,
            'description': itemType.description,
            'quantity': replacementRequest.quantity,
            'status': replacementRequest.status 
        })
    return items


if not ReplacementRequest.table_exists():
    ReplacementRequest.create_table()
    print("Table 'ReplacementRequest' created")
