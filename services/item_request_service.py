from peewee import *
from models.item_request import ItemRequest
from services.item_type_service import createItemType, getItemType
from services.item_service import getItem, createItem
from models.item import Item


def createItemRequest(id, name, description, quantity, owner) -> None:
    if id:
        type = Item.get_by_id(id).type
    else:
        type = createItemType(name, description)
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

