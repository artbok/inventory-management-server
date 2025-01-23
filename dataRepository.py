from peewee import *


db = SqliteDatabase('data.db')


class User(Model):
    id = AutoField()
    name = CharField()
    password = CharField()
    rightsLevel = IntegerField()
    class Meta:
        database = db
        only_save_dirty = True


def createUser(name, password, rightsLevel):
    User.create(name = name, password = password, rightsLevel = rightsLevel).save()


def getUser(name) -> User:
    return User.get_or_none(User.name == name)


def isAdmin(name, password):
    user: User = getUser(name)
    if not user or user.password != password:
        return 'authError'
    if user.rightsLevel < 2:
        return 'accessError'
    return 'ok'


def isUser(name, password):
    user: User = getUser(name)
    if user and user.password == password:
        return True
    return False


def getUsers():
    users = []
    for user in User.select().where(User.rightsLevel == 1):
        users.append(user.name)
    return users


if not User.table_exists():
    User.create_table()
    createUser("bebra", "12345", 2)
    createUser("bebrobruh", "12345", 1)
    print("Table 'User' created")


#add status
class Items(Model):
    id = AutoField()
    name = CharField()
    description = CharField(null=True)
    quantity = IntegerField()
    quantityInStorage = IntegerField()
    class Meta:
        database = db
        only_save_dirty = True


def getItem(name, description) -> Items:
    return Items.get_or_none(Items.name == name, Items.description == description)


def createItem(name, description, quantity):
    item: Items = getItem(name, description)
    if not item:
        Items.create(name = name, description = description, quantity = quantity, quantityInStorage = quantity).save()
    else:
        item.quantity += quantity
        item.quantityInStorage += quantity
        item.save()


def getStorageItemsOnPage(page) -> list[Items]:
    items = []
    for item in Items.select().paginate(page, 10):
        items.append({
            'name': item.name,
            'quantity': item.quantity,
            'quantityInStorage': item.quantityInStorage,
            'description': item.description
        })
    return items


if not Items.table_exists():
    Items.create_table()
    createItem("Золотой тунец", "легендарный", 99)
    for i in range(1, 52):
        createItem(f"Item{i}", str(i**2), 100-i)
    print("Table 'Items' created")


class ItemsRequests(Model):
    id = AutoField()
    isCustom = BooleanField()
    itemName = CharField()
    quantity = IntegerField()
    owner = CharField()
    status = CharField(default = "created")
    # openedDate = DateField()
    # closedDate = DateField()
    class Meta:
        database = db
        only_save_dirty = True


def createItemRequest(isCustom, itemName, quantity, owner):
    ItemsRequests.create(isCustom = isCustom, itemName = itemName, quantity = quantity, owner = owner).save()


def getItemsRequests(owner):
    itemsRequests = []
    for itemRequest in ItemsRequests.select().where(ItemsRequests.owner == owner):
        itemsRequests.append({
            'itemName': itemRequest.itemName,
            'quantity': itemRequest.quantity,
            'status': itemRequest.status
        })
    return itemsRequests


if not ItemsRequests.table_exists():
    ItemsRequests.create_table()
    print("Table 'ItemsRequests' created")


class ItemOwners(Model):
    id = AutoField()
    owner = CharField()
    itemName = CharField()
    description = CharField(null=True)
    quantity = IntegerField()
    class Meta:
        database = db
        only_save_dirty = True


def getItemOwner(owner, itemName, description):
    return ItemOwners.get_or_none(ItemOwners.owner == owner, ItemOwners.itemName == itemName, ItemOwners.description == description)


def addOwnerForItem(owner, itemName, description, quantity):
    item: Items = getItem(itemName, description)
    item.quantityInStorage -= quantity
    item.save()
    itemOwner = getItemOwner(owner, itemName, description)
    if not itemOwner:
        ItemOwners.create(owner = owner, itemName = itemName, description = description, quantity = quantity).save()
    else:
        itemOwner.quantity += quantity
        itemOwner.save()


def getUsersItems(owner, page):
    usersItems = []
    for userItem in ItemOwners.select().where(ItemOwners.owner == owner).paginate(page, 10):
        usersItems.append({
            'itemName': userItem.itemName,
            'description': userItem.description,
            'quantity': userItem.quantity,
        })
    return usersItems


if not ItemOwners.table_exists():
    ItemOwners.create_table()
    print("Table 'ItemOwners' created")


class ReplacementsRequests(Model):
    id = AutoField()
    owner = CharField()
    itemName = CharField()
    quantity = IntegerField()
    status = CharField(default='created')
    class Meta:
        database = db
        only_save_dirty = True


def createReplacementRequest(owner, itemName, description, quantity):
    item: ItemOwners = getItemOwner(owner, itemName, description)
    item.quantity -= quantity
    if item.quantity == 0:
        item.delete_instance()
    item: Items = getItem(itemName, description)
    item.quantity -= quantity
    if item.quantity == 0:
        item.delete_instance()
    ReplacementsRequests.create(owner = owner, itemName = itemName, quantity = quantity).save()


def getReplacementsRequests(owner):
    replacementsRequests = []
    for replacementRequest in ReplacementsRequests.select().where(ReplacementsRequests.owner == owner):
        replacementsRequests.append({
            'itemName': replacementRequest.itemName,
            'quantity': replacementRequest.quantity,
            'status': replacementRequest.status 
        })
    return replacementsRequests

if not ReplacementsRequests.table_exists():
    ReplacementsRequests.create_table()
    print("Table 'ReplacementsRequests' created")