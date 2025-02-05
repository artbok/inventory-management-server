from peewee import *
from models.item_type import ItemType


def getItemType(type) -> ItemType:
    return ItemType.get_or_none(ItemType.type == type)


def createItemType(name, description, status="Новый") -> ItemType:
    itemType: ItemType = ItemType.get_or_none(ItemType.name == name, ItemType.description == description, ItemType.status == status)
    if not itemType:
        return ItemType.create(name = name, description = description, status = status)
    return itemType


if not ItemType.table_exists():
    ItemType.create_table()
    print("Table 'Item' created")
