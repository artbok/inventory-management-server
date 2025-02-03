from peewee import *
from models.item_request import ItemRequest


def createItemRequest(type, itemName, itemDescription, itemQuantity, owner) -> None:
    ItemRequest.create(type = type, itemName = itemName, itemDescription = itemDescription, itemQuantity = itemQuantity, owner = owner)


def getItemsRequests(owner) -> list[ItemRequest]:
    if owner == None:
        itemsRequests = ItemRequest.select()
    else:
        itemsRequests = ItemRequest.select().where(ItemRequest.owner == owner)
    requests = []
    for itemRequest in itemsRequests:
        requests.append({
            'type': itemRequest.type,
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

