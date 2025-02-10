from peewee import *
from models.item import Item
from services.item_type_service import getItemType, createItemType
from services.report_service import createReport

def getItem(owner, type) -> Item:
    return Item.get_or_none(Item.owner == owner, Item.type == type)


def createItem(owner, type, quantity) -> Item:
    item = getItem(owner, type)
    if not item:
       return Item.create(owner = owner, type = type, quantity = quantity)
    item.quantity += quantity
    item.save()
    return item


def editItem(itemId, newName, newDescription, newQuantity) -> None:
    item: Item = Item.get_by_id(itemId)
    status = getItemType(item.type).status
    itemType = createItemType(newName, newDescription, status)
    item.type = itemType.type
    item.quantity = newQuantity
    item.save()
   


def deleteItem(itemId, quantity):
    item: Item = Item.get_by_id(itemId)
    item.quantity -= quantity
    item.save()
 
    if item.quantity == 0:
        item.delete_instance()

    

def giveItem(itemId, quantity, user):
    item: Item = Item.get_by_id(itemId)
    item.quantity -= quantity
    item.save()
    createItem(user, item.type, quantity)

def changeStatus(itemId, quantity, status):
    item: Item = Item.get_by_id(itemId)
    curItemType = getItemType(item.type)
    newItemType = createItemType(curItemType.name, curItemType.description, status)
    item.quantity -= quantity
    item.save()
    createItem(item.owner, newItemType.type, quantity)
    if item.quantity == 0:
        item.delete_instance()
    


def getUserItems(owner, page) -> list[map]:
    userItems = []
    for userItem in Item.select().where(Item.owner == owner).paginate(page, 10):
        type = userItem.type
        itemType = getItemType(type)
        userItems.append({
            'id': userItem.id,
            'type': type,
            'name': itemType.name,
            'description': itemType.description,
            'quantity': userItem.quantity,
            'status': itemType.status
        })
    return userItems


def getStorageItemsOnPage(page) -> list[map]:
    items = []
    for item in Item.select().where(Item.owner == None).paginate(page, 10):
        type = item.type
        itemType = getItemType(type)
        items.append({
            'id': item.id,
            'type': type,
            'name': itemType.name,
            'description': itemType.description,
            'quantity': item.quantity,
            'status': itemType.status
        })
    return items


if not Item.table_exists():
    Item.create_table()
    print("Table 'ItemOwner' created")
