from peewee import *
from models.planing import Planing


def createPlaning(itemName, itemDescription, itemQuantity, supplier, price):
    planing: Planing = Planing.get_or_none(Planing.itemName == itemName, Planing.itemDescription == itemDescription, Planing.supplier == supplier, Planing.price == price)
    if planing:
        planing.itemQuantity += itemQuantity
        planing.save()
    else:
        Planing.create(itemName = itemName, itemDescription = itemDescription, itemQuantity = itemQuantity, supplier = supplier, price = price)


def changePlanningStatus(id, completed):
    planing: Planing = Planing.get_by_id(id)
    planing.completed = completed
    planing.save()


def getPlanings():
    uncompletedPlannings = []
    for planing in Planing.select().where(Planing.completed == False):
        uncompletedPlannings.append({
            'id': planing.id,
            'itemName': planing.itemName,
            'itemDescription': planing.itemDescription,
            'itemQuantity': planing.itemQuantity,
            'supplier': planing.supplier,
            'price': planing.price,
            'completed': planing.completed
        })
    completedPlannings = []
    for planing in Planing.select().where(Planing.completed == True):
        completedPlannings.append({
            'id': planing.id,
            'itemName': planing.itemName,
            'itemDescription': planing.itemDescription,
            'itemQuantity': planing.itemQuantity,
            'supplier': planing.supplier,
            'price': planing.price,
            'completed': planing.completed
        })
    return completedPlannings, uncompletedPlannings



if not Planing.table_exists():
    Planing.create_table()
    print("Table 'Planing' created")