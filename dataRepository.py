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
        order_by = ['name']


def createUser(name, password, rightsLevel):
    User.create(name = name, password = password, rightsLevel = rightsLevel).save()


def getUser(name) -> User:
    return User.get_or_none(User.name == name)


def isAdmin(name, password) -> str:
    user: User = getUser(name)
    if not user or user.password != password:
        return 'authError'
    if user.rightsLevel < 2:
        return 'accessError'
    return 'ok'


def isUser(name, password) -> bool:
    user: User = getUser(name)
    if user and user.password == password:
        return True
    return False


def getUsers() -> list[User]:
    users = []
    for user in User.select().where(User.rightsLevel == 1):
        users.append(user.name)
    return users


if not User.table_exists():
    User.create_table()
    createUser("bebra", "12345", 2)
    createUser("bebrobruh", "12345", 1)
    print("Table 'User' created")


class Items(Model):
    id = AutoField()
    name = CharField()
    description = CharField(null=True)
    quantity = IntegerField()
    quantityInStorage = IntegerField()
    status = CharField(default="Новый")
    class Meta:
        database = db
        only_save_dirty = True
        order_by = ['name']


def getItem(id) -> Items:
    return Items.get_or_none(Items.id == id)


def createItem(name, description, quantity) -> None:
    item: Items = Items.get_or_none(Items.name == name, Items.description == description)
    if not item:
        Items.create(name = name, description = description, quantity = quantity, quantityInStorage = quantity).save()
    else:
        item.quantity += quantity
        item.quantityInStorage += quantity
        item.save()


def editItem(itemId, newName, newQuantity, newDescription) -> None:
    item: Items = getItem(itemId)
    item.name = newName
    item.description = newDescription
    item.quantityInStorage = newQuantity - (item.quantity - item.quantityInStorage)
    item.quantity = newQuantity
    item.save()
    for itemOwner in ItemOwners.select().where(ItemOwners.itemId == itemId):
        itemOwner.itemName = newName
        itemOwner.description = newDescription
        itemOwner.save()


def changeStatus(itemId, quantity, status):
    curItem: Items = getItem(itemId)
    curItem.quantity -= quantity
    curItem.quantityInStorage -= quantity
    curItem.save()
    item: Items = Items.get_or_none().where(Items.id == itemId, Items.status == status)
    if item:
        item.quantity += quantity
        item.quantityInStorage += quantity
        item.save()
    else:
        Items.create(name = curItem.name, description = curItem.description, quantity = quantity, quantityInStorage = quantity, status = status)
    if curItem.quantity == 0:
        curItem.delete_instance()


def getStorageItemsOnPage(page) -> list[Items]:
    items = []
    for item in Items.select().paginate(page, 10):
        items.append({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'quantity': item.quantity,
            'quantityInStorage': item.quantityInStorage,
            "status": item.status
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
    itemId = IntegerField(null=True)
    itemName = CharField()
    itemDescription = CharField()
    itemQuantity = IntegerField()
    owner = CharField()
    status = CharField(default="Ожидает ответа")
    class Meta:
        database = db
        only_save_dirty = True
        order_by = ['owner']


def createItemRequest(itemId, itemName, itemDescription, itemQuantity, owner):
    ItemsRequests.create(itemId = itemId, itemName = itemName, itemDescription = itemDescription, itemQuantity = itemQuantity, owner = owner).save()


def getItemsRequests(owner):
    if owner == None:
        itemsRequests = ItemsRequests.select()
    else:
        itemsRequests = ItemsRequests.select().where(ItemsRequests.owner == owner)
    requests = []
    for itemRequest in itemsRequests:
        requests.append({
            'itemId': itemRequest.itemId,
            'itemName': itemRequest.itemName,
            'itemDescription': itemRequest.itemDescription,
            'itemQuantity': itemRequest.itemQuantity,
            'owner': itemRequest.owner,
            'status': itemRequest.status
        })
    return requests


if not ItemsRequests.table_exists():
    ItemsRequests.create_table()
    print("Table 'ItemsRequests' created")


class ItemOwners(Model):
    id = AutoField()
    owner = CharField()
    itemId = IntegerField()
    itemName = CharField()
    itemDescription = CharField(null=True)
    itemQuantity = IntegerField()
    itemStatus = CharField(default="Используемый")
    class Meta:
        database = db
        only_save_dirty = True
        order_by = ['owner']


def getItemOwner(owner, itemId):
    return ItemOwners.get_or_none(ItemOwners.owner == owner, ItemOwners.itemId == itemId)


def addOwnerForItem(owner, itemId, quantity):
    item: Items = getItem(itemId)
    item.quantityInStorage -= quantity
    item.save()
    itemOwner = getItemOwner(owner, itemId)
    if not itemOwner:
        ItemOwners.create(owner = owner, itemId = itemId, itemName = item.name, itemDescription = item.description, itemQuantity = quantity).save()
    else:
        itemOwner.quantity += quantity
        itemOwner.save()


def getUsersItems(owner, page):
    usersItems = []
    for userItem in ItemOwners.select().where(ItemOwners.owner == owner).paginate(page, 10):
        usersItems.append({
            'id': userItem.itemId,
            'name': userItem.itemName,
            'description': userItem.itemDescription,
            'quantity': userItem.itemQuantity,
        })
    return usersItems


if not ItemOwners.table_exists():
    ItemOwners.create_table()
    print("Table 'ItemOwners' created")


class ReplacementsRequests(Model):
    id = AutoField()
    owner = CharField()
    itemId = IntegerField()
    itemName = CharField()
    itemDescription = CharField(null=True)
    itemQuantity = IntegerField()
    status = CharField(default='created')
    class Meta:
        database = db
        only_save_dirty = True
        order_by = ['owner']


def createReplacementRequest(owner, itemId, quantity):
    request: ReplacementsRequests = ReplacementsRequests.get_or_none().where(ReplacementsRequests.itemId == itemId, ReplacementsRequests.owner == owner, ReplacementsRequests.status == "created")
    if request:
        request.itemQuantity += quantity
        request.save()
    else:
        ReplacementsRequests.create(owner = owner, itemId = itemId, itemName = item.name, itemDescription = item.description, itemQuantity = quantity).save()
    itemOwner: ItemOwners = getItemOwner(owner, itemId)
    itemOwner.itemQuantity -= quantity
    itemOwner.save()
    if itemOwner.itemQuantity == 0:
        itemOwner.delete_instance()
    item: Items = getItem(itemId)
    item.quantity -= quantity
    item.save()
    if item.quantity == 0:
        item.delete_instance()


def getReplacementsRequests(owner):
    items = []
    if owner == None:
        requests = ReplacementsRequests.select()
    else:
        requests = ReplacementsRequests.select().where(ReplacementsRequests.owner == owner)
    
    for replacementRequest in requests:
        items.append({
            'itemName': replacementRequest.itemName,
            'description': replacementRequest.itemDescription,
            'quantity': replacementRequest.itemQuantity,
            'status': replacementRequest.status 
        })
    return items

if not ReplacementsRequests.table_exists():
    ReplacementsRequests.create_table()
    print("Table 'ReplacementsRequests' created")

class Stats(Model):
    id = AutoField()
    totalItemsGiven = IntegerField(default=0)
    totalReplacements = IntegerField(default=0)
    class Meta:
        database = db
        only_save_dirty = True

if not Stats.table_exists():
    Stats.create_table()
    print("Table 'Stats' created")

