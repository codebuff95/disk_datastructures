from random import randint
from io import StringIO
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
        out.write('Account Number: ' + str(self.acc_no) +'\nHolder Name: '+ str(self.holder_name) + '\nCreated On: ' + str(self.created_on) + '\n')
        out.write('Transactions: ')
        for transaction in self.transactions:
            out.write(str(transaction) + '\n')
        return out.getvalue()
