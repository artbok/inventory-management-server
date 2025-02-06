from peewee import *
from models.item_request import ItemRequest
from services.item_type_service import createItemType, getItemType
from services.item_service import getItem, createItem
from models.item import Item


def createItemRequest(id, name, description, quantity, owner) -> None:
    if id:
        type = Item.get_by_id(id).type
    else:
        type = createItemType(name, description).type
    itemRequest: ItemRequest = ItemRequest.get_or_none(ItemRequest.owner == owner, ItemRequest.type == type, ItemRequest.status == 'Ожидает ответа')
    if itemRequest:
        itemRequest.quantity += quantity
        itemRequest.save()
    else: 
        ItemRequest.create(type = type, quantity = quantity, owner = owner)


def getItemsRequests(owner) -> list[ItemRequest]:
    if owner == None:
        itemsRequests = ItemRequest.select()
    else:
        itemsRequests = ItemRequest.select().where(ItemRequest.owner == owner)
    requests = []
    for itemRequest in itemsRequests:
        itemType = getItemType(itemRequest.type)
        requests.append({
            'id': itemRequest.id,
            'name': itemType.name,
            'description': itemType.description,
            'quantity': itemRequest.quantity,
            'owner': itemRequest.owner,
            'status': itemRequest.status
        })
    return requests


def getStorageItems(username, page) -> list[map]:
    items = []
    for item in Item.select().where(Item.owner == None).paginate(page, 10):
        type = item.type
        itemType = getItemType(type)
        requestsCounter= 0
        itemRequest = ItemRequest.get_or_none(ItemRequest.type == type, ItemRequest.owner == username, ItemRequest.status == "Ожидает ответа")
        if itemRequest:
            requestsCounter += itemRequest.quantity
        items.append({
            'id': item.id,
            'type': type,
            'name': itemType.name,
            'description': itemType.description,
            'quantity': item.quantity,
            'status': itemType.status,
            'requestsCounter': requestsCounter
        })
    return items

def acceptItemRequest(id):
    request: ItemRequest = ItemRequest.get_by_id(id)
    itemType = getItemType(request.type)
    item = getItem(None, request.type)
    quantity = 0
    if item:
        quantity = item.quantity
    
    required = {"name": itemType.name, "description": itemType.description, "quantity": request.quantity - quantity}
    
    if not item or item.quantity < request.quantity:
        return 'notEnoughItems', required
    
    item.quantity -= request.quantity
    item.save()
    if item.quantity == 0:
        item.delete_instance()

    request.status = "Одобрено"
    request.save()
    
    createItem(request.owner, request.type, request.quantity)
    return 'ok', None


def declineItemRequest(id):
    request: ItemRequest = ItemRequest.get_by_id(id)
    request.status = "Отклонено"
    request.save()


if not ItemRequest.table_exists():
    ItemRequest.create_table()
    print("Table 'ItemRequest' created")

