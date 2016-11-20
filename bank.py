from random import randint
from io import StringIO
from prettytable import PrettyTable

bank_f_n = 'data/bank.sf'
acc_f_n = 'data/accounts_data.sf'
acc_create_log_f_n = 'data/create.log'

class Transaction:
    def __init__(self,amount,when):
        self.amount = amount
        self.time_stamp = when
    def __str__(self):
        return '(Amount: ' + str(self.amount) + ',Time Stamp: ' + str(self.time_stamp) + ')'
class Account:
    def __init__(self,acc_no,holder_name,created_on):
        self.acc_no = acc_no
        self.holder_name = holder_name
        self.created_on = created_on
        self.transactions = []
    def make_transaction(self,my_transaction):
        ins_index = 0

        while ins_index < len(self.transactions) and my_transaction.time_stamp < self.transactions[ins_index].time_stamp:
            ins_index += 1
        self.transactions.insert(ins_index,my_transaction)
    def get_new_acc_no():
        s = ''
        for i in range(16):
            s += str(randint(0,9))
        return s
    def __str__(self):
        out = StringIO()
        out.write('Account Details:\n')
        t = PrettyTable(['Account Attribute', 'Value'])
        t.add_row(['Acc Number',str(self.acc_no)])
        t.add_row(['Holder Name',str(self.holder_name)])
        t.add_row(['Created On',str(self.created_on)])
        out.write(str(t) + '\n\nAccount Transactions:\n')
        t = PrettyTable(['Time', 'Amount'])
        for transaction in self.transactions:
            t.add_row([transaction.time_stamp,transaction.amount])
        out.write(str(t) + '\n\n')
        return out.getvalue()
