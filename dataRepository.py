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


class ItemRequests(Model):
    id = AutoField()
    isCustom = BooleanField()
    itemid = IntegerField()
    amount = IntegerField()
    name = CharField()
    status = CharField()
    openedDate = DateField()
    closedDate = DateField()
    class Meta:
        database = db
        only_save_dirty = True

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
    itemId = IntegerField()
    amount = IntegerField()
    class Meta:
        database = db
        only_save_dirty = True
