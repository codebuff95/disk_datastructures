import btree,bank,datetime,time,shelve,sys
from btree_errors import *
from random import randint,random
def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    example: randomDate("1/1/2010 12:00 AM", "1/1/2016 12:00 AM", random.random())
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))
def randomDate(start, end, prop = random()):
    return strTimeProp(start, end, '%m/%d/%Y %I:%M %p', prop)
with open('data/first_names') as fn_f:
    fnames = [line.strip() for line in fn_f]
with open('data/last_names') as ln_f:
    lnames = [line.strip() for line in ln_f]
bank_f_n = 'data/bank.sf'
acc_f_n = 'data/accounts_data.sf'
acc_create_log_f_n = 'data/create.log'
def generate_random_account():
    global fnames,lnames
    holder_name = fnames[randint(0,len(fnames)-1)] + ' ' + lnames[randint(0,len(lnames)-1)]
    new_acc_no = bank.Account.get_new_acc_no()
    my_acc = bank.Account(new_acc_no,holder_name,randomDate("1/1/2009 12:00 AM", "1/1/2010 12:00 AM"))
    no_of_trans = randint(3,10)
    for t in range(no_of_trans):
        amount = randint(500,1000)
        if random() <= 0.5:
            amount *= -1
        my_acc.make_transaction(bank.Transaction(amount,randomDate("1/1/2010 12:00 AM", "1/1/2016 12:00 AM")))
    return my_acc
    #print(my_acc)
    #print(new_acc_no,' ',holder_name)

def create_single_account(my_acc):
    """ returns the number of disk accesses taken for account creation """
    global acc_f_n, bank_f_n
    with btree.BTree(bank_f_n) as my_bt, shelve.open(acc_f_n,writeback=True) as ad_sf, open(acc_create_log_f_n,'at',encoding='utf-8') as acc_create_log_f:
        try:
            no_of_accounts = ad_sf['no_of_accounts']
        except KeyError:
            ad_sf['no_of_accounts'] = 0
            no_of_accounts = 0
        my_acc = generate_random_account()
        acc_create_log_f.write(my_acc.acc_no + ' ' + my_acc.holder_name + '\n')
        ad_sf[str(no_of_accounts+1)] = my_acc
        ad_sf['no_of_accounts'] = no_of_accounts+1
        return my_bt.insert_key(my_acc.acc_no,str(no_of_accounts+1))

def start_bulk_creation(n):
    global acc_f_n, bank_f_n
    """ n = number of accounts to be created.
        returns total number of disk accesses taken to insert the n elements.
    """
    #sys.stdout = open('data/acc_creation.log','at',encoding='utf-8')
    with btree.BTree(bank_f_n) as my_bt, shelve.open(acc_f_n,writeback=True) as ad_sf, open(acc_create_log_f_n,'at',encoding='utf-8') as acc_create_log_f:
        try:
            no_of_accounts = ad_sf['no_of_accounts']
        except KeyError:
            ad_sf['no_of_accounts'] = 0
            no_of_accounts = 0
        i = 0
        d_a_c = 0
        while i < n:
            i += 1
            my_acc = generate_random_account()
            acc_create_log_f.write(my_acc.acc_no + ' ' + my_acc.holder_name + '\n')
            ad_sf[str(no_of_accounts+i)] = my_acc
            ad_sf['no_of_accounts'] = no_of_accounts+i
            d_a_c += my_bt.insert_key(my_acc.acc_no,str(no_of_accounts+i))
        return d_a_c
