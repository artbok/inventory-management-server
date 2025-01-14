from peewee import *

db = SqliteDatabase('data.db')

class User(Model):
    id = AutoField()
    username = CharField()
    password = CharField()
    rightsLevel = IntegerField()
    class Meta:
        database = db
        only_save_dirty = True

if not User.table_exists():
    User.create_table()
    User.create(username = "bebra", password = "12345", rightsLevel = 2).save()
    print("Table 'User' created")

def getUser(username) -> User:
    return User.get_or_none(User.username == username)

def isAdmin(username, password):
    user: User = getUser(username)
    if not user or user.password != password:
        return 'passwordOrUsernameIsIncorrect'
    if user.rightsLevel < 2:
        return 'accessError'
    return 'ok'

def isUser(username, password):
    user: User = getUser(username)
    if user and user.password == password:
        return True
    return False

#add status
class Items(Model):
    id = AutoField()
    name = CharField()
    description = CharField()
    amount = IntegerField()
    class Meta:
        database = db
        only_save_dirty = True

if not Items.table_exists():
    Items.create_table()
    print("Table 'Items' created")

def createItem(name, description, amount):
    item: Items = Items.get_or_none(Items.name == name, Items.description == description)
    if not item:
        Items.create(name = name, description = description, amount = amount).save()
    else:
        item.amount += amount
        item.save()


def getItemsOnPage(n, owner: None) -> list[Items]:
    items = []
    if owner:
        source = Items.select().where(Items.owner == name).paginate(n, 10)
    else:
        source = Items.select().paginate(n, 10)
    for item in source:
        items.append({
            'name': item.name,
            'amount': str(item.amount),
            'description': item.description
        })
    return items


class ItemsRequests(Model):
    id = AutoField()
    isCustom = BooleanField()
    itemName = CharField()
    amount = IntegerField()
    owner = CharField()
    status = CharField()
    # openedDate = DateField()
    # closedDate = DateField()
    class Meta:
        database = db
        only_save_dirty = True


def getItemsRequests(owner):
    itemsRequests = []
    for itemRequest in ItemsRequests.select().where(ItemsRequests.owner == owner):
        itemsRequests.append({
            'name': itemRequest.name,
            'amount': str(itemRequest.amount),
            'status': itemRequest.status
        })
    return itemsRequests


class ItemOwners(Model):
    id = AutoField()
    ownerId = IntegerField()
    itemId = IntegerField()
    amount = IntegerField()
    class Meta:
        database = db
        only_save_dirty = True

class ReplacementsRequests(Model):
    id = AutoField()
    owner = CharField()
    itemName = CharField()
    amount = IntegerField()
    status = CharField()
    class Meta:
        database = db
        only_save_dirty = True


def getReplacementsRequests(owner):
    replacementsRequests = []
    for replacementRequest in ReplacementsRequests.select().where(ReplacementsRequests.owner == owner):
        replacementsRequests.append({
            'itemName': replacementRequest.itemName,
            'amount': replacementRequest.amount,
            'status': replacementRequest.status 
        })
    return replacementsRequests