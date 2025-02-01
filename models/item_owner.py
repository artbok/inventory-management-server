from peewee import *
from .database import BaseModel
from .item import *


class ItemOwner(BaseModel):
    id = AutoField()
    owner = CharField()
    itemId = IntegerField()
    itemName = CharField()
    itemDescription = CharField(null=True)
    itemQuantity = IntegerField()
    itemStatus = CharField(default="Используемый")


def getItemOwner(owner, itemId) -> ItemOwner:
    return ItemOwner.get_or_none(ItemOwner.owner == owner, ItemOwner.itemId == itemId)


def addOwnerForItem(owner, itemId, quantity):
    item: Item = Item.get_by_id(itemId)
    item.quantityInStorage -= quantity
    item.save()
    itemOwner = getItemOwner(owner, itemId)
    if not itemOwner:
        ItemOwner.create(owner = owner, itemId = itemId, itemName = item.name, itemDescription = item.description, itemQuantity = quantity).save()
    else:
        itemOwner.itemQuantity += quantity
        itemOwner.save()


def getUsersItems(owner, page):
    usersItems = []
    for userItem in ItemOwner.select().where(ItemOwner.owner == owner).paginate(page, 10):
        usersItems.append({
            'id': userItem.itemId,
            'name': userItem.itemName,
            'description': userItem.itemDescription,
            'quantity': userItem.itemQuantity,
        })
    return usersItems


if not ItemOwner.table_exists():
    ItemOwner.create_table()
    print("Table 'ItemOwner' created")
