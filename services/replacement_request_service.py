from peewee import *
from models.replacement_request import ReplacementRequest
from services.item_type_service import getItemType, createItemType
from services.item_service import createItem, Item, getItem

def createReplacementRequest(owner, itemId, quantity):
    item: Item = Item.get_by_id(itemId)
    item.quantity -= quantity
    item.save()
    
    itemType = getItemType(item.type)
    newItemType = createItemType(itemType.name, itemType.description, "Сломанный")
    if item.quantity == 0:
        item.delete_instance()
    item = createItem(owner, newItemType.type, quantity)
    
    request: ReplacementRequest = ReplacementRequest.get_or_none(ReplacementRequest.itemId == item.id, ReplacementRequest.owner == owner)
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


def acceptReplacementRequest(id):
    request: ReplacementRequest = ReplacementRequest.get_by_id(id)
    request.status = "Одобрено"
    request.save()
    item: Item = Item.get_by_id(request.itemId)
    curItemType = getItemType(item.type)
    newItemType = createItemType(curItemType.name, curItemType.description)
    newItem = getItem(request.owner, newItemType.type)
    if newItem:
        newItem.quantity += request.quantity
        newItem.save()
    else:
        createItem(request.owner, newItemType.type, request.quantity)
    item.quantity -= request.quantity
    item.save()
    if item.quantity == 0:
        item.delete_instance()


def declineReplacementRequest(id):
    request: ReplacementRequest = ReplacementRequest.get_by_id(id)
    request.status = "Отклонено"
    request.save()


if not ReplacementRequest.table_exists():
    ReplacementRequest.create_table()
    print("Table 'ReplacementRequest' created")
