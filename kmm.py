import datetime
import json
import pendulum


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
# # amount of money for goal
# # description of goal
# # date by which goal should be met
###
class SavingGoal:
    def __init__(self, amount, desc, dueDate=None):
        self.amount = amount
        self.desc = desc
        self.dueDate = [dueDate] # dueDate can be changed in a list format

    # this function can change due date while preserving change log
    def changeDueDate(self, dueDate):
        self.dueDate.append(dueDate)


###
# class that stores a specific date
# # the date to be stored
###
class Date():
    def __init__(self, date=pendulum.now('UTC')):
        self.date = date

    # increment timezone by one day
    def next(self):
        return Date(self.date.add(days=1))

    # for converting timezones (used to display in eastern time)
    def asTZ(self, tag='UTC'):
        return pendulum.timezone(tag).convert(self.date)


###
# class for storing amount of money
# # amount of money, in USD
### may not be implemented if btc not needed
class Amount():
    def __init__(self, usd):
        self.usd = usd

    def __add__(self, i):
        self.usd += i

    def __sub__(self, i):
        self.usd -= i

    def __mul__(self, n):
        self.usd *= n

    def __idiv__(self, n):
        self.usd /= n


###
# class for storing crypto amount
# # amount
# # currency name
###
class CryptoAmount():
    def __init__(self, a=0, c='BTC'):
        self.amount = a
        self.currency = c

    def setEquiv(self, eqv):
        self.eqv = eq

###
# class that holds check deposit information
# also known as a one-time-payment
# # amount gained
# # sender of money
# # date of transfer
###
class OneTimePayment:
    def __init__(self, amount, sender=Entity(), date=Date()):
        self.date = date
        self.sender = sender
        self.amount = amount
        self.isDeposited = False

    # updates the deposit status (used to say whether or not this value should be taken into consideraiton at a given time)
    def deposit(self):
        self.isDeposited = True

    def subtractFee(self, a):
        self.amount.subtract(a)


class TimePeriod:
    def __init__(self, start=pendulum.now('UTC'), end=pendulum.now('UTC').add(days=1)):
        self.start = start
        self.end = end

    def periodExpires(self):
        return self.end is not -1

    def isActive(self, d1=None):
        if d1 == None:
            d1 = pendulum.now('UTC')
        return self.start <= d1 and (self.end == -1 or d1 <= self.end)


class MonthlyIncome:
    def __init__(self, amount, e=Entity(), p=TimePeriod()):
        self.period = p
        self.amount = amount  # income every month

    def isActive(self, d1=None):
        return self.time.isActive(d1)


class Entity:
    def __init__(self, name='nil'):
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


class MonthlyExpense:
    def __init__(self, amount, e=Entity(), p=TimePeriod()):
        self.amount = amount
        self.entity = e
        self.period = p
