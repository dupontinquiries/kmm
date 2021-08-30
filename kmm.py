import datetime
import json


class CommandInterpreter:
    def __init__(self):
        self.initModel()

    def createModel():
        print("TODO CommandInterpreter.createModel")


class FileLoader:
    def __init__(self):
        print("Created a file loader")

    def load(fName, type='json'):
        if type == 'json':
            return json.load(fName)


###
# class that holds saving goals
###
class SavingGoal:
    def __init__(self, amount, desc, date):
        self.amount = amount
        self.desc = desc
        self.date = date


class Check:
    def __init__(self, sender, amount, date=None):
        if date == None:
            self.date = datetime.datetime
        self.sender = sender
        self.amount = amount
        self.isDeposited = False

    def deposit(self):
        self.isDeposited = True


class TimePeriod:
    def __init__(self, start=None, end=None):
        if start == None and end == None:
            start = -1
            end = -1
        else:
            self.start = start
            self.end = end

    def periodExpires(self):
        return self.end != -1

    def isActive(self, d1=None):
        if d1 == None:
            d1 = datetime.datetime
        return self.start <= d1 and (self.end == -1 or d1 <= self.end)


class MonthlyIncome:
    def __init__(self, amount, p=TimePeriod()):
        self.time = p
        self.amount = amount  # income every month

    def isActive(self, d1=None):
        return self.time.isActive(d1)


class Entity:
    def __init__(self, name):
        self.name = name
        self.links = []

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < self.other

    def __repr__(self):
        return self.name

    def setLink(self, link):
        self.append(link)

    def getLink(self):
        return None if len(self.links) == 0 else self.links[-1]


class Expense:
    def __init__(self, amount, desc, date=None):
        if date == None:
            self.date = datetime.datetime
        self.amount = amount
        self.isPaid = False
        self.desc = desc
        self.entity = None

    def setPaid(self):
        self.isPaid = True

    def setEntity(self, entity):
        self.entity = entity
