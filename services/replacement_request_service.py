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
    
    request: ReplacementRequest = ReplacementRequest.get_or_none(ReplacementRequest.type == newItemType.type, ReplacementRequest.owner == owner)
    if request:
        request.quantity += quantity
        request.save()
    else:
        ReplacementRequest.create(owner = owner, type = newItemType.type, quantity = quantity)
    


def getReplacementsRequests(owner):
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
            'status': replacementRequest.status, #should be deleted
            'id': replacementRequest.id
        })
    return items


def acceptReplacementRequest(id):
    item = getItem(None, "Новый")
    request: ReplacementRequest = ReplacementRequest.get_by_id(id)
    curItemType = getItemType(request.type)
    required = {"name": curItemType.name, "description": curItemType.description, "quantity": request.quantity - item.quantity}
    
    if not item or item.quantity < request.quantity:
        return 'notEnoughItems'

    request.status = "Одобрено" #accept request
    request.save()

    curItemType = getItemType(request.type)    #substract quantity
    item = getItem(request.owner, request.type)
    item.quantity -= request.quantity
    item.save()
    if item.quantity == 0:
        item.delete_instance()
    
    newItemType = createItemType(curItemType.name, curItemType.description) #create new item
    createItem(request.owner, newItemType.type, request.quantity)
    return 'ok'


def declineReplacementRequest(id):
    request: ReplacementRequest = ReplacementRequest.get_by_id(id)
    request.status = "Отклонено"
    request.save()


if not ReplacementRequest.table_exists():
    ReplacementRequest.create_table()
    print("Table 'ReplacementRequest' created")
