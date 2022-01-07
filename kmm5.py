import datetime
import json
import pendulum
import copy

# class TransactionLogger:
#     def __init__(self):
#         self.chron = [] # the chronological order of transactions

#     def __repr__(self):
#         return "LOG:\n" + "\n\t".join(self.chron)

#     def log(self, action):
#         pass

#     def export(self, hh=None):
#         if hh is None:
#             return str(self.chron)
#         else:
#             pass

# class CommandInterpreter:
#     def __init__(self):
#         self.initModel()

#     def createModel():
#         print("TODO CommandInterpreter.createModel")


# class FileLoader:
#     def __init__(self):
#         print("Created a file loader")

#     def load(fName, type='json'):
#         if type == 'json':
#             return json.load(fName)


###
# class that holds saving goals
# # amount of money for goal
# # description of goal
# # date by which goal should be met
###
class SavingGoal: #### TODO: IMPLEMENT Account.project()::isGoalMet(Goal g)
                  ####[may be useful but may be replaced by a balance check function]
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
# whole class is redundant because pendulum lib already has this functionality
# class Date:
#     def __init__(self, date=pendulum.now('UTC')):
#         self.date = date

#     # increment timezone by one day
#     def next(self):
#         return Date(self.date.add(days=1))

#     def next(self):
#         return Date(self.date.subtract(days=1))

#     # for converting timezones (useful for displaying eastern time)
#     def asTZ(self, tag='UTC'):
#         return pendulum.timezone(tag).convert(self.date)


###
# class for storing amount of money
# # amount of money
# # type of currency
### may not be implemented if btc not needed
class Amount:
    def __init__(self, a, t='USD'):
        self.a = a
        self.t = t

    def getNumberAmount(self):
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

# whole class may be replaced by a dict() that contains all the important information
class Entity:
    def __init__(self, name=None):
        self.data = dict()
        self.data['name'] = name

    # x for hashing
    # def __repr__(self):
    #     return self.name # could be dangerous if trying to have separate purchases from the same entity

    # x for sorting entities in a list
    # def __eq__(self, other):

    # def wd(self, k, v): # writes to data (repetitive since this is written in python)
        # self.data['k'] = v

    def getName(self):
        return self.data['name']

    def sameName(self, o):
        if issubclass(type(o), Entity):
            return self.data['name'] == o.data['name']
        else: # assume string input and parse data
            return self.data['name'] == o

    def __lt__(self, other):
        return self.name < self.other

    # def __gt__(self, other):
    #     return self.name > self.other

    # for adding a webpage, phone number, etc. to an entity

    def setLink(self, link):
        self.links.append(link)

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
class OneTimePayment: #### TODO: IMPLEMENT THIS CLASS IN Account::project
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


# class TimePeriod:
#     def __init__(self, start=None, end=None):
#         self.start = start
#         self.end = end

#     def hasEnd(self):
#         return self.end is not None

#     def isActive(self, d1=None):
#         if d1 is None:
#             d1 = pendulum.now('UTC')
#         return self.start <= d1 and (self.end is None or d1 <= self.end)

#     def extendTo(self, e):
#         self.end = e

#     def getEnd(self):
#         return self.end


###
# Periodic Amounts can be used to project into the future
## amount
## the sender
## the active period (will pay as long as within this period)
## the period between deposits (not smooth)
###
class PeriodicAmount:
    def __init__(self, a, e=None, ap=None, p=None):
        if issubclass(type(a), Amount):
            self.amount = a.getNumberAmount()
            self.t = a.currency()
        else:
            self.amount = a  # adjustment amount that happens at the end of every period
            self.t = None
        self.entity = e # entity w/ purchase data
        self.activePeriod = ap # pendulum tuple
        self.period = p # pendulum duration

    # def __init__(self, a, e=None, ap=None, p=None):
    #     if issubclass(type(a), Amount):
    #         self.amount = a.getNumberAmount()
    #         self.t = a.currency()
    #     else:
    #         self.amount = a  # adjustment amount that happens at the end of every period
    #         self.t = None
    #     self.entity = e
    #     self.activePeriod = ap
    #     if issubclass(type(p), TimePeriod): # pass through for time period
    #         self.period = p
    #     else: # assume string and try to parse the data with pendulum
    #         pass

    def t_before_end(self, t):
        return self.activePeriod[1] is None or t <= self.activePeriod[1]

    def t_within(self, t):
        return (self.activePeriod[0] is None or t >= self.activePeriod[0]) and self.t_before_end(t)

    def getValue():
        return Amount(self.amount, self.t)

    def getNumberAmount(self):
        return self.amount

    def getPeriod(self):
        return self.period

    def getActivePeriod(self):
        return self.activePeriod

    # def hasEnd(self):
    #     return self.activePeriod is None #or self.activePeriod.hasEnd()

    def currency(self):
        return self.t

    # def isActive(self, d1=None):
    #     return self.time.isActive(d1)


# class MonthlyIncome(PeriodicAmount):
#     def __init__(self, a, e=None, ap=None):
#         PeriodicAmount.__init__(self, a, e, ap, pendulum.duration(months=1))


# class Expense:
#     def __init__(self, amount, desc, date=None):
#         if date == None:
#             self.date = datetime.datetime
#         self.amount = amount
#         self.isPaid = False
#         self.desc = desc
#         self.entity = None

#     def setPaid(self):
#         self.isPaid = True

#     def setEntity(self, entity):
#         self.entity = entity


# class MonthlyExpense:
#     def __init__(self, amount, e=Entity(), p=TimePeriod()):
#         self.amount = amount
#         self.entity = e
#         self.period = p


class Account:
    def __init__(self, ib=None, t=None):
        # not sure whether to require default type for self.t
        # could be annoying to work around later on
        self.balance = dict()
        if t is not None:
            if ib is None:
                self.balance[t] = 0
            elif issubclass(type(ib), Amount):
                self.balance[t] = ib.getNumberAmount()
            else:
                self.balance[t] = ib
        self.pbal = None # copy.deepcopy(self.balance)
        self.projections = []
        # print(f'init: {self.balance}')

    def __repr__(self):
        return self.balance

    def getCurrency(self):
        return self.t

    def getCurrencies(self):
        return self.balance.keys()

    def getBalance(self, k=None):
        if k is None:
            return self.balance
        if k not in self.balance:
            # potential vector for overload (make millions of unique requests to fill memory)
            self.balance[k] = 0
        return self.balance[k]

    def addAmount(self, a):
        if a.currency() not in self.balance:
            self.balance[a.currency()] = 0
        self.balance[a.currency()] += a.getNumberAmount()

    def deposit(self, i, k=None):
        if k is None:
            k = list(self.balance.keys())[0]
        self.balance[k] += i

    def getProjectedBalance(self, k=None):
        if k is None:
            return self.pbal
        if k not in self.pbal:
            # potential vector for overload (make millions of unique requests to fill memory)
            self.pbal[k] = 0
        return self.pbal[k]

    def addProjection(self, pi):
        self.projections.append(pi)

    def legacy_project(self, et, t=None): # endtime
        tStart = t
        self.pbal = dict()
        self.pbal = copy.deepcopy(self.getBalance())
        for p in self.projections:
            # for each projection, iterate until hit end
            if issubclass(type(p), PeriodicAmount):
                if tStart is None: # start from today
                    t = pendulum.today()
                ### print(max(t, p.getActivePeriod()[0]))
                ### print(min(et, p.getActivePeriod()[1]))
                n = 0
                _n = 0
                while t <= et and p.t_before_end(t):
                    if p.currency() not in self.pbal:
                        self.pbal[p.currency()] = 0
                    if p.t_within(t):
                        ### print(f' + added {p.getNumberAmount()} on {t}')
                        self.pbal[p.currency()] += p.getNumberAmount()
                        n += 1
                    _n += 1
                    t += p.period
                ### print(f'true n: {n} ({_n})')
        return self

    def project(self, et, t=None):

        # _t = t
        # if _t is None:
        #     _t = pendulum.today()

        if t is None:
            t = pendulum.today()


        self.pbal = dict()
        for k, v in self.balance.items():
            self.pbal[k] = v
        # self.pbal = copy.deepcopy(self.balance)

        # print(self.pbal)


        for p in self.projections:

            n = 0

            fu = p.getActivePeriod()[0]

            while fu < t:
                # print(f'    fu -> {fu}')
                fu += p.getPeriod()
            
            lu = fu + p.getPeriod()

            while p.t_before_end(lu) and lu <= et:
                # print(f'    lu -> {lu}')
                lu += p.getPeriod()

            n += (lu - fu).total_seconds() / p.getPeriod().total_seconds()

            if p.currency() not in self.pbal:
                self.pbal[p.currency()] = 0
            self.pbal[p.currency()] += p.getNumberAmount() * int(n)

            # print(f' + n: {n}')
            # print(f' - start: {fu}, end: {lu}')
            # print(f' - pbal: {self.pbal}')

        return self

    def project_threaded_helper(self, et, t, p):

        n = 0

        fu = p.getActivePeriod()[0]

        while fu < t:
            # print(f'    fu -> {fu}')
            fu += p.getPeriod()
        
        lu = fu + p.getPeriod()

        while p.t_before_end(lu) and lu <= et:
            # print(f'    lu -> {lu}')
            lu += p.getPeriod()

        n += (lu - fu).total_seconds() / p.getPeriod().total_seconds()

        if p.currency() not in self.pbal:
            self.pbal[p.currency()] = 0
        self.pbal[p.currency()] += p.getNumberAmount() * int(n)


    def project_threaded(self, et, t=None):

        import concurrent.futures

        if t is None:
            t = pendulum.today()

        self.pbal = dict()
        for k, v in self.balance.items():
            self.pbal[k] = v

        executor = concurrent.futures.ProcessPoolExecutor(6)
        futures = [executor.submit(self.project_threaded_helper, self, et, t, p)
                   for p in self.projections]
        concurrent.futures.wait(futures)

        return self


# test if two values are equal within a margin of error
def epsilon(a, b, e):
    return abs(a - b) < e


if __name__ == "__main__":

    print()
    print("testing")
    print()

    ##

    # tests

    ##

    current_test = "saving account projections"
    print(f"testing [{current_test}]")

    acc1 = Account(0, 'USD')
    i1 = PeriodicAmount(Amount(1200, 'USD'), None, (pendulum.today(), pendulum.today().add(months=24)), pendulum.duration(months=1))
    acc1.addProjection(i1)
    acc1.project(pendulum.today().add(months=3))
    assert acc1.getBalance('USD') == 0
    assert acc1.getProjectedBalance('USD') == 3 * 1200

    i2 = PeriodicAmount(Amount(1750.50, 'USD'), None, (pendulum.today().add(weeks=2), pendulum.today().add(months=8)), pendulum.duration(weeks=2))
    acc2 = Account(4500, 'USD')
    acc2.addProjection(i2)
    
    acc2.project(pendulum.today().add(weeks=2))
    assert acc2.getBalance('USD') == 4500
    assert acc2.getProjectedBalance('USD') == 4500 + 1750.50
    
    acc2.project(pendulum.today().add(weeks=3))
    assert acc2.getProjectedBalance('USD') == 4500 + 1750.50
    
    acc2.project(pendulum.today().add(weeks=4))
    assert acc2.getProjectedBalance('USD') == 4500 + (2 * 1750.50)

    acc2.project(pendulum.today().add(weeks=5))
    assert acc2.getProjectedBalance('USD') == 4500 + (2 * 1750.50)

    print(f"finished testing [{current_test}]\n")

    #
    ###
    #

    current_test = "saving account projections (advanced)"
    print(f"testing [{current_test}]")

    acc3 = Account()
    acc4 = Account(4500, 'USD')
    i3 = PeriodicAmount(Amount(600, 'USD'), None, (pendulum.today(), pendulum.today().add(months=1)), pendulum.duration(months=1))
    acc3.addProjection(i3)

    assert acc3.getBalance('USD') == 0
    assert acc4.getBalance('USD') == 4500

    acc3.project(pendulum.today().add(days=1))
    assert acc3.getBalance('USD') == 0
    assert acc3.project(pendulum.today().add(days=1)).getProjectedBalance('USD') == 600
    assert acc3.project(pendulum.today().add(months=1)).getProjectedBalance('USD') >= 600

    i4 = PeriodicAmount(Amount(100, 'USD'), None, (pendulum.tomorrow(), pendulum.tomorrow().add(months=5)), pendulum.duration(months=1))
    acc3.addProjection(i3)

    assert acc4.getBalance('USD') == 4500
    assert acc4.project(pendulum.today().add(days=1)).getBalance('USD') == 4500    

    # the second and third month are outside the active period, so the payment should only happen today and today+1mo
    assert acc3.project(pendulum.today().add(months=3)).getProjectedBalance('USD') == 1200
    assert acc3.project(pendulum.today().add(months=8)).getProjectedBalance('USD') == 1200

    print(f"finished testing [{current_test}]\n")

    #
    ###
    #

    current_test = "saving account projections (advanced)"
    print(f"testing [{current_test}]")
    acc5 = Account()
    i5 = PeriodicAmount(Amount(600, 'USD'), None, (pendulum.today(), pendulum.today().add(months=1)), pendulum.duration(months=1))
    acc5.addProjection(i5)
    i6 = PeriodicAmount(Amount(10, 'ETH'), None, (pendulum.today(), pendulum.today().add(days=5)), pendulum.duration(days=1))
    acc5.addProjection(i6)
    i7 = PeriodicAmount(Amount(100, 'IOT'), None, (pendulum.today(), pendulum.today().add(days=5)), pendulum.duration(days=1))
    acc5.addProjection(i7)

    acc5.project(pendulum.today().add(months=3))

    assert acc5.getProjectedBalance('USD') == 600
    assert acc5.getProjectedBalance('ETH') == 60
    assert acc5.getProjectedBalance('IOT') == 600
    
    print(f"finished testing [{current_test}]\n")

    #
    ###
    #

    current_test = "saving account projections (advanced 2)"
    print(f"testing [{current_test}]")

    acc6 = Account(400.50, 'USD')
    i8 = PeriodicAmount(Amount(900.50, 'USD'), None, (pendulum.tomorrow(), pendulum.today().add(months=8)), pendulum.duration(months=1))
    acc6.addProjection(i8)
    assert acc6.project(pendulum.today().add(months=3)).getProjectedBalance('USD') == (400.50 + (2 * 900.50)) or acc6.project(pendulum.today().add(months=3)).getProjectedBalance('USD') == (400.50 + (3 * 900.50))
    assert acc6.project(pendulum.today().add(months=3, days=3)).getProjectedBalance('USD') == (400.50 + (3 * 900.50))

    print(f"finished testing [{current_test}]\n")

    #
    ##
    #

    current_test = "saving account faster projections (time vs regular projections)"    
    print(f"testing [{current_test}]")

    from datetime import datetime
    n_iter = 5
    n_size = 200
    start_time = datetime.now()
    for i in range(n_iter):
        if i % 10 == 0:
            print(f'\t iter {i}')
        acc7 = Account()
        import random
        rl = list(random.randint(0, 145) / 200. for j in range(n_size))
        assert len(rl) == n_size
        for n in rl:
            i9 = PeriodicAmount(Amount(n, 'USD'), None, (pendulum.tomorrow(), None), pendulum.duration(months=1))
            acc7.addProjection(i9)
        # print(acc7.project(pendulum.today().add(years=5, days=2)).getProjectedBalance('USD'))
        acc7.project(pendulum.today().add(years=5, days=2)).getProjectedBalance('USD')
        # assert epsilon( acc7.project(pendulum.today().add(years=5, days=5)).getProjectedBalance('USD'), sum(rl) * 12. * 5., .0001)

        # for n in rl[:10]:
        #     i9 = PeriodicAmount(Amount(n, 'ETH'), None, (pendulum.tomorrow(), None), pendulum.duration(months=1))
        #     acc7.addProjection(i9)
        # assert epsilon( acc7.project(pendulum.today().add(months=3)).getProjectedBalance('USD'), sum(rl) * 3., .0001)
        # assert epsilon( acc7.project(pendulum.today().add(months=3)).getProjectedBalance('ETH'), sum(rl[:10]) * 3., .0001)
        # assert epsilon( acc7.project(pendulum.today().add(years=30)).getProjectedBalance('ETH'), sum(rl[:10]) * 12. * 30., .0001)
    end_time = datetime.now()
    t1 = end_time - start_time
    start_time = datetime.now()
    for i in range(n_iter):
        if i % 10 == 0:
            print(f'\t iter {i}')
        acc7 = Account()
        import random
        rl = list(random.randint(0, 145) / 200. for j in range(n_size))
        assert len(rl) == n_size
        for n in rl:
            i9 = PeriodicAmount(Amount(n, 'USD'), None, (pendulum.tomorrow(), None), pendulum.duration(months=1))
            acc7.addProjection(i9)
        # print(acc7.legacy_project(pendulum.today().add(years=5, days=2)).getProjectedBalance('USD'))
        acc7.legacy_project(pendulum.today().add(years=5, days=2)).getProjectedBalance('USD')
        # assert epsilon( acc7.project(pendulum.today().add(years=5, days=5)).getProjectedBalance('USD'), sum(rl) * 12. * 5., .0001)

        # for n in rl[:10]:
        #     i9 = PeriodicAmount(Amount(n, 'ETH'), None, (pendulum.tomorrow(), None), pendulum.duration(months=1))
        #     acc7.addProjection(i9)
        # assert epsilon( acc7.project(pendulum.today().add(months=3)).getProjectedBalance('USD'), sum(rl) * 3., .0001)
        # assert epsilon( acc7.project(pendulum.today().add(months=3)).getProjectedBalance('ETH'), sum(rl[:10]) * 3., .0001)
        # assert epsilon( acc7.project(pendulum.today().add(years=30)).getProjectedBalance('ETH'), sum(rl[:10]) * 12. * 30., .0001)
    end_time = datetime.now()
    t2 = end_time - start_time

    start_time = datetime.now()
    for i in range(n_iter):
        if i % 10 == 0:
            print(f'\t iter {i}')
        acc7 = Account()
        import random
        rl = list(random.randint(0, 145) / 200. for j in range(n_size))
        assert len(rl) == n_size
        for n in rl:
            i9 = PeriodicAmount(Amount(n, 'USD'), None, (pendulum.tomorrow(), None), pendulum.duration(months=1))
            acc7.addProjection(i9)
        # print(acc7.legacy_project(pendulum.today().add(years=5, days=2)).getProjectedBalance('USD'))
        acc7.project_threaded(pendulum.today().add(years=5, days=2)).getProjectedBalance('USD')

    end_time = datetime.now()
    t3 = end_time - start_time

    print(f' time elapsed: {t1} vs. {t2} vs, {t3}')

    print(f"finished testing [{current_test}]\n")

    #
    ##
    #