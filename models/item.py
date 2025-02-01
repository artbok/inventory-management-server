from peewee import *
from .database import BaseModel
from .item_owner import ItemOwner


class Item(BaseModel):
    id = AutoField()
    name = CharField()
    description = CharField(null=True)
    quantity = IntegerField()
    quantityInStorage = IntegerField()
    status = CharField(default="Новый")

def getItem(id) -> Item:
    return Item.get_or_none(Item.id == id)


def createItem(name, description, quantity) -> None:
    item: Item = Item.get_or_none(Item.name == name, Item.description == description)
    if not item:
        Item.create(name = name, description = description, quantity = quantity, quantityInStorage = quantity).save()
    else:
        item.quantity += quantity
        item.quantityInStorage += quantity
        item.save()


def editItem(itemId, newName, newQuantity, newDescription) -> None:
    item: Item = Item.get_by_id(itemId)
    item.name = newName
    item.description = newDescription
    item.quantityInStorage = newQuantity - (item.quantity - item.quantityInStorage)
    item.quantity = newQuantity
    item.save()
    for itemOwner in ItemOwner.select().where(ItemOwner.itemId == itemId):
        itemOwner.itemName = newName
        itemOwner.description = newDescription
        itemOwner.save()


def changeStatus(itemId, quantity, status):
    curItem: Item = Item.get_by_id(itemId)
    curItem.quantity -= quantity
    curItem.quantityInStorage -= quantity
    curItem.save()
    item: Item = Item.get_or_none(Item.id == itemId, Item.status == status)
    if item:
        item.quantity += quantity
        item.quantityInStorage += quantity
        item.save()
    else:
        Item.create(name = curItem.name, description = curItem.description, quantity = quantity, quantityInStorage = quantity, status = status)
    if curItem.quantity == 0:
        curItem.delete_instance()


def getStorageItemsOnPage(page) -> list[Item]:
    items = []
    for item in Item.select().paginate(page, 10):
        items.append({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'quantity': item.quantity,
            'quantityInStorage': item.quantityInStorage,
            "status": item.status
        })
    return items


if not Item.table_exists():
    Item.create_table()
    createItem("Золотой тунец", "легендарный", 99)
    for i in range(1, 52):
        createItem(f"Item{i}", str(i**2), 100-i)
    print("Table 'Item' created")
