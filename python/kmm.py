import datetime
import json
import pendulum
import copy

class TransactionLogger:
    def __init__(self):
        self.chron = [] # the chronological order of transactions

    def __repr__(self):
        return "LOG:\n" + "\n\t".join(self.chron)

    def log(self, action):
        pass

    def export(self, hh=None):
        if hh is None:
            return str(self.chron)
        else:
            pass

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
class Date:
    def __init__(self, date=pendulum.now('UTC')):
        self.date = date

    # increment timezone by one day
    def next(self):
        return Date(self.date.add(days=1))

    def next(self):
        return Date(self.date.subtract(days=1))

    # for converting timezones (useful for displaying eastern time)
    def asTZ(self, tag='UTC'):
        return pendulum.timezone(tag).convert(self.date)


###
# class for storing amount of money
# # amount of money
# # type of currency
### may not be implemented if btc not needed
class Amount:
    def __init__(self, a, t='USD'):
        self.a = a
        self.t = t

    def getAmount(self):
        return self.a

    def currency(self):
        return self.t

    def __repr__(self):
        return (f'[{self.t}] {self.a}')
        # return self.a

    # def __str__(self):
    #     return (f'[{self.t}] {self.a}')

    def check(self):
        if self.a < 0:
            raise ValueError('An amount fell below zero!')

    def __add__(self, i):
        if issubclass(type(i), Amount) and i.t == self.t: # isinstance throws an error
            self.a += i.a
        else:
            try:
                self.a += i
            except:
                raise ValueError(f'Failed to add unknown type {type(i)} to an amount of type {self.t}')
        # self.check()
        return self

    def __sub__(self, i):
        if issubclass(type(i), Amount) and i.t == self.t:
            self.a -= i.a
        else:
            try:
                self.a -= i
            except:
                raise ValueError(f'Failed to subtract unknown type {type(i)} from an amount of type {self.t}')
        # self.check()
        return self

    def __eq__(self, o):
        if issubclass(type(o), Amount):
            return self.a == o.a and self.t == o.t
        else:
            return self.a == o

    def __lt__(self, o):
        if issubclass(type(o), Amount):
            if self.t == o.t:
                return self.a < o.a
            else:
                return None
        else:
            return self.a < o

    def __gt__(self, o):
        if issubclass(type(o), Amount):
            if self.t == o.t:
                return self.a > o.a
            else:
                return None
        else:
            return self.a > o

    # can add support for add/sub diff currencies later

    def __mul__(self, n):
        self.a *= n
        return self

    # def __idiv__(self, n):
    #     self.a /= n


class Entity:
    def __init__(self, name=None):
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


###
# class for storing crypto amount
# # amount
# # currency name
###
class CryptoAmount(Amount): # inheritance
    def __init__(self, a, t='ETH'):
        Amount.__init__(self, a, t)
        self.a = a
        self.t = t

    # will add support for auto conversions if needed


###
# class that holds check deposit information
# also known as a one-time-payment
# # amount gained (class Amount)
# # sender of money
# # date of transfer
###
class OneTimePayment:
    def __init__(self, amount, sender=None, date=None):

        self.amount = amount
        self.isDeposited = False
        
        if sender is None:
            self.sender = Entity()
        else:
            self.sender = sender

        if date is None:
            self.sender = Date()
        else:
            self.date = sender
        

    # updates the deposit status (used to say whether or not this value should
    # be taken into consideraiton at a given time)
    def deposit(self):
        self.isDeposited = True

    def subtractFee(self, a): # subtract takes in a number
        self.amount -= a


class TimePeriod:
    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end
        # if start is None:
        #     self.start = pendulum.now('UTC')
        # else:
        #     self.start = start

        # if end is None:
        #     self.end = pendulum.now('UTC').add(days=1)
        # else:
        #     self.end = end

    def forever(self):
        return self.end is None

    def periodExpires(self):
        return self.end is not None

    def isActive(self, d1=None):
        if d1 is None:
            d1 = pendulum.now('UTC')
        # print(f'start -> {self.start}')
        # print(f'd1    -> {d1}')
        # print(f'end   -> {self.end}')
        # print(d1)
        # print(self.end)
        return self.start <= d1 and (self.end is None or d1 <= self.end)

    def extendTo(self, e):
        self.end = e

    def getEnd(self):
        return self.end


###
# Periodic Incomes can be used to project into the future
## amount
## the sender
## the active period (will pay as long as within this period)
## the period between deposits (not smooth)
###
class PeriodicIncome:
    def __init__(self, a, e=None, ap=None, p=None):
        if issubclass(type(a), Amount):
            self.amount = a.getAmount()
            self.t = a.currency()
        else:
            self.amount = a  # income every month
        self.entity = e
        self.activePeriod = ap
        self.period = p

    def getAmount(self):
        return Amount(self.amount, self.t)

    def forever(self):
        return self.activePeriod.forever()

    def getCurrency(self):
        return self.t

    def isActive(self, d1=None):
        return self.time.isActive(d1)


class MonthlyIncome(PeriodicIncome):
    def __init__(self, a, e=None, ap=None):
        PeriodicIncome.__init__(self, a, e, ap, pendulum.duration(months=1))


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


class SavingAccount:
    def __init__(self, ib = 0, t='USD'):
        self.t = t
        self.balance = dict()
        if ib is None:
            self.balance[t] = 0
        elif issubclass(type(ib), Amount):
            self.balance[t] = ib.getAmount()
        else:
            self.balance[t] = ib

    def __repr__(self):
        return self.balance

    def getCurrency(self):
        return self.t

    def deposit(self, i, k=None):
        if k is None:
            k = self.t
        self.balance[k] += i

    def getBalance(self, k=None):
        if k is None:
            return self.balance
        return self.balance[k]


class ProjectableAccount:
    def __init__(self, acc=None):
        if acc is None:
            self.account = SavingAccount()
            # self.account = copy.deepcopy(SavingAccount())
        else:
            self.account = acc
        # self.pbal = dict()
        self.pbal = copy.deepcopy(self.account.balance)
        self.projections = []

    def getBalance(self, k=None):
        if k is None:
            return self.account.balance
        return self.account.balance[k]

    def getProjectedBalance(self, k=None):
        if k is None:
            return self.pbal
        if k not in self.pbal:
            self.pbal[k] = 0
        return self.pbal[k]

    def addIncome(self, pi):
        self.projections.append(pi)

    def project(self, et): # endtime
        self.pbal = dict()
        self.pbal = copy.deepcopy(self.getBalance())
        for p in self.projections:
            # for each projection, iterate until hit end
            if issubclass(type(p), PeriodicIncome):
                t = pendulum.today()
                while (p.forever() and t < et) or (not p.forever() and t < p.activePeriod.getEnd() and t < et):
                    t += p.period
                    if p.getCurrency() not in self.pbal:
                        self.pbal[p.getCurrency()] = 0
                    self.pbal[p.getCurrency()] += p.getAmount().getAmount()
        return self


# test if two values are equal within a margin of error
def epsilon(a, b, e):
    return abs(a - b) < e


if __name__ == "__main__":

    print("testing")

    ##

    # tests

    ##

    current_test = "amounts"
    print(f"testing [{current_test}]")
    amount1 = Amount(100, 'USD')
    amount2 = Amount(100, 'USD')
    assert amount1.a == 100
    assert amount2.a == 100
    amount1 + amount2
    assert amount1.a == 200
    assert amount2.a == 100
    amount1 += 100
    assert amount1.a == 300
    assert amount2.a == 100
    amount1 -= 100
    amount2 += 25
    assert amount1.a == 200
    assert amount2.a == 125
    assert amount2.getAmount() == 125
    assert amount2.currency() == 'USD'
    print(f"finished testing [{current_test}]\n")

    #
    ###
    #

    current_test = "crypto amounts"
    print(f"testing [{current_test}]")
    crypto1 = CryptoAmount(15, t='ETH')
    crypto2 = CryptoAmount(15, t='ETH')
    assert (crypto1 - crypto2).a == 0
    assert crypto1.t == crypto2.t
    try:
        amount1 + crypto1
        print('failed')
        assert False
    except:
        assert True
    print(f"finished testing [{current_test}]\n")

    #
    ###
    #

    current_test = "advanced money - comparisons"
    print(f"testing [{current_test}]")
    amount3 = Amount(100, 'USD')
    amount4 = Amount(100, 'USD')
    assert amount3 == amount4
    amount5 = Amount(200, 'USD')
    assert amount5.a > amount3.a
    assert amount5 > amount3
    print(f"finished testing [{current_test}]\n")

    #
    ###
    #

    current_test = "advanced money - decimals"
    print(f"testing [{current_test}]")
    amount3 = Amount(20.22, 'USD')
    amount4 = Amount(20.22, 'USD')
    assert amount3.a == amount4.a
    assert amount3 == amount4
    amount5 = Amount(20.23, 'USD')
    assert amount5.a > amount3.a
    assert amount5 > amount3
    print(f"finished testing [{current_test}]\n")

    #
    ###
    #

    current_test = "time periods (pendulum library)"
    print(f"testing [{current_test}]")
    d1 = pendulum.today()
    d2 = pendulum.today()
    assert d1 == d1
    d1.add(weeks=1)
    assert d1 == d2
    d2 = d2.add(days=1)
    assert d1 != d2
    assert d1 < d2
    assert d1 <= d2 
    print(f"finished testing [{current_test}]\n")
    
    #
    ###
    #

    current_test = "time periods (timeperiod class)"
    print(f"testing [{current_test}]")
    # print(pendulum.now())
    assert type(pendulum.now()) is not type("")
    tp1 = TimePeriod(pendulum.today(), None)
    tp2 = TimePeriod(pendulum.today(), pendulum.today().add(days=1))
    # print(f'tp1: {tp1}')
    # print(f'tp2: {tp2}')
    assert tp1.isActive() is True
    assert tp2.isActive() is True
    assert tp1.isActive(pendulum.today().add(seconds=2)) is True
    assert tp1.isActive(pendulum.today().add(days=2)) is True
    assert tp2.isActive(pendulum.today().add(weeks=2)) is False
    tp2.extendTo(tp2.getEnd().add(weeks=3))
    assert tp2.isActive(pendulum.today().add(weeks=2)) is True
    print(f"finished testing [{current_test}]\n")

    #
    ###
    #

    current_test = "buying an item using a savings account"
    print(f"testing [{current_test}]")
    acc1 = SavingAccount(0, 'USD')
    acc2 = SavingAccount(4500, 'USD')
    assert acc1.getBalance('USD') == 0
    assert acc2.getBalance('USD') < 5000
    assert acc2.getBalance('USD') < Amount(10000.70, 'USD')
    acc1.deposit(450)
    assert acc1.getBalance('USD') == 450
    assert acc2.getBalance('USD') - acc1.getBalance('USD') > 0
    print(f"finished testing [{current_test}]\n")

    #
    ###
    #

    current_test = "saving account projections"
    print(f"testing [{current_test}]")
    acc1 = SavingAccount(0, 'USD')
    acc2 = SavingAccount(4500, 'USD')
    i1 = MonthlyIncome(Amount(1200, 'USD'))
    i2 = MonthlyIncome(Amount(1750.50, 'USD'))
    assert acc1.getBalance('USD') == 0
    print(f"finished testing [{current_test}]\n")

    #
    ###
    #

    current_test = "saving account projections (advanced)"
    print(f"testing [{current_test}]")
    acc1 = ProjectableAccount(SavingAccount(0, 'USD'))
    acc2 = ProjectableAccount(SavingAccount(4500, 'USD'))
    i3 = MonthlyIncome(Amount(600, 'USD'), None, TimePeriod(pendulum.today(), pendulum.today().add(months=1)))
    acc1.addIncome(i3)
    assert acc1.getBalance('USD') == 0
    assert acc2.getBalance('USD') == 4500
    assert acc1.project(pendulum.today().add(days=1)).getBalance('USD') == 0 ### says 600
    assert acc1.project(pendulum.today().add(months=1)).getBalance('USD') == 0 ### says 600
    assert acc1.project(pendulum.today().add(months=1)).getProjectedBalance('USD') == 600
    assert acc1.project(pendulum.today().add(months=3)).getProjectedBalance('USD') == 600
    print(f"finished testing [{current_test}]\n")

    #
    ###
    #

    current_test = "saving account projections (advanced 2)"
    print(f"testing [{current_test}]")
    acc3 = ProjectableAccount(SavingAccount(400.50, 'USD'))
    i4 = MonthlyIncome(Amount(900.50, 'USD'), None, TimePeriod(pendulum.today(), pendulum.today().add(months=8)))
    acc3.addIncome(i4)
    assert acc3.project(pendulum.today().add(months=3)).getProjectedBalance('USD') == (400.50 + (3 * 900.50))
    print(f"finished testing [{current_test}]\n")

    #
    ###
    #

    current_test = "saving account projections (advanced 3)"
    print(f"testing [{current_test}]")
    for i in range(10):
        if i % 10 == 0:
            print(f'\t iter {i}')
        acc4 = ProjectableAccount(SavingAccount(0, 'USD'))
        import random
        rl = list(random.randint(0, 145) / 200. for j in range(35))
        assert len(rl) == 35
        for n in rl:
            i5 = MonthlyIncome(Amount(n, 'USD'), None, TimePeriod(pendulum.today()))
            acc4.addIncome(i5)
        assert epsilon( acc4.project(pendulum.today().add(years=5)).getProjectedBalance('USD'), sum(rl) * 12. * 5., .0001)
        for n in rl[:10]:
            i5 = MonthlyIncome(CryptoAmount(n, 'ETH'), None, TimePeriod(pendulum.today()))
            acc4.addIncome(i5)
        assert epsilon( acc4.project(pendulum.today().add(months=3)).getProjectedBalance('USD'), sum(rl) * 3., .0001)
        assert epsilon( acc4.project(pendulum.today().add(months=3)).getProjectedBalance('ETH'), sum(rl[:10]) * 3., .0001)
        assert epsilon( acc4.project(pendulum.today().add(years=30)).getProjectedBalance('ETH'), sum(rl[:10]) * 12. * 30., .0001)
    print(f"finished testing [{current_test}]\n")


    # l = TransactionLogger()
    # l.export('log.json')