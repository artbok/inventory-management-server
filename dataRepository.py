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


def createUser(username, password, rightsLevel):
    User.create(username = username, password = password, rightsLevel = rightsLevel).save()


def getUser(username) -> User:
    return User.get_or_none(User.username == username)


def isAdmin(username, password):
    user: User = getUser(username)
    if not user or user.password != password:
        return 'authError'
    if user.rightsLevel < 2:
        return 'accessError'
    return 'ok'


def isUser(username, password):
    user: User = getUser(username)
    if user and user.password == password:
        return True
    return False

if not User.table_exists():
    User.create_table()
    createUser("bebra", "12345", 2)
    print("Table 'User' created")


#add status
class Items(Model):
    id = AutoField()
    name = CharField()
    description = CharField(null=True)
    amount = IntegerField()
    class Meta:
        database = db
        only_save_dirty = True


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


if not Items.table_exists():
    Items.create_table()
    createItem("Золотой тунец", "легендарный", 99)
    print("Table 'Items' created")


class ItemsRequests(Model):
    id = AutoField()
    isCustom = BooleanField()
    itemName = CharField()
    amount = IntegerField()
    owner = CharField()
    status = CharField(default = "created")
    # openedDate = DateField()
    # closedDate = DateField()
    class Meta:
        database = db
        only_save_dirty = True


def createItemRequest(isCustom, itemName, amount, owner):
    Items.create(isCustom = isCustom, itemName = itemName, amount = amount, owner = owner).save()


def getItemsRequests(owner):
    itemsRequests = []
    for itemRequest in ItemsRequests.select().where(ItemsRequests.owner == owner):
        itemsRequests.append({
            'name': itemRequest.name,
            'amount': str(itemRequest.amount),
            'status': itemRequest.status
        })
    return itemsRequests


if not ItemsRequests.table_exists():
    ItemsRequests.create_table()
    print("Table 'ItemsRequests' created")


class ItemOwners(Model):
    id = AutoField()
    onwer = CharField()
    itemName = CharField()
    amount = IntegerField()
    class Meta:
        database = db
        only_save_dirty = True


class ReplacementsRequests(Model):
    id = AutoField()
    owner = CharField()
    itemName = CharField()
    amount = IntegerField()
    status = CharField(default='created')
    class Meta:
        database = db
        only_save_dirty = True


def createReplacementRequest(owner, itemName, amount):
    ReplacementsRequests.create(owner = owner, itemName = itemName, amount = amount)


def getReplacementsRequests(owner):
    replacementsRequests = []
    for replacementRequest in ReplacementsRequests.select().where(ReplacementsRequests.owner == owner):
        replacementsRequests.append({
            'itemName': replacementRequest.itemName,
            'amount': replacementRequest.amount,
            'status': replacementRequest.status 
        })
    return replacementsRequests


if not ReplacementsRequests.table_exists():
    ReplacementsRequests.create_table()
    print("Table 'ReplacementsRequests' created")