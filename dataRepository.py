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
    print("Table 'User' created")

def getUser(username) -> User:
    return User.get_or_none(User.username == username)

class Items(Model):
    id = AutoField()
    name = CharField()
    description = CharField()
    amount = IntegerField()
    class Meta:
        database = db
        only_save_dirty = True
    
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