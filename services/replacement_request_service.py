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
    
    request: ReplacementRequest = ReplacementRequest.get_or_none(ReplacementRequest.type == newItemType.type, ReplacementRequest.owner == owner, ReplacementRequest.status == "Ожидает ответа")
    if request:
        request.quantity += quantity
        request.save()
    else:
        ReplacementRequest.create(owner = owner, type = newItemType.type, quantity = quantity)
    


def getReplacementRequests(owner):
    items = []
    if owner == None:
        requests = ReplacementRequest.select()
    else:
        requests = ReplacementRequest.select().where(ReplacementRequest.owner == owner)
    
    for replacementRequest in requests:
        itemType = getItemType(replacementRequest.type)
        items.append({
            'name': itemType.name,
            'description': itemType.description,
            'quantity': replacementRequest.quantity,
            'status': replacementRequest.status, 
            'id': replacementRequest.id
        })
    return items


def acceptReplacementRequest(id):
    request: ReplacementRequest = ReplacementRequest.get_by_id(id)
    curItemType = getItemType(request.type)
    newItemType = createItemType(curItemType.name, curItemType.description)
    item = getItem(None, newItemType.type)
    quantity = 0
    if item:
        quantity = item.quantity
    
    required = {"name": curItemType.name, "description": curItemType.description, "quantity": request.quantity - quantity}
    
    if not item or item.quantity < request.quantity:
        return 'notEnoughItems', required
    item.quantity -= request.quantity
    item.save()
    createItem(None, request.type, request.quantity)
    request.status = "Одобрено" 
    request.save()
    
    item = getItem(request.owner, request.type)
    item.quantity -= request.quantity
    item.save()
    if item.quantity == 0:
        item.delete_instance()
    createItem(request.owner, newItemType.type, request.quantity)
    return 'ok', None


def declineReplacementRequest(id):
    request: ReplacementRequest = ReplacementRequest.get_by_id(id)
    request.status = "Отклонено"
    request.save()


if not ReplacementRequest.table_exists():
    ReplacementRequest.create_table()
    print("Table 'ReplacementRequest' created")
