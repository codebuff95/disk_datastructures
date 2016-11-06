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
def randomDate(start, end, prop):
    return strTimeProp(start, end, '%m/%d/%Y %I:%M %p', prop)
if __name__ == '__main__':
    with open('data/first_names') as fn_f:
        fnames = [line.strip() for line in fn_f]
    with open('data/last_names') as ln_f:
        lnames = [line.strip() for line in ln_f]
    sys.stdout = open('data/acc_creation.log','at',encoding='utf-8')
    with btree.BTree('data/bank.sf') as my_bt, shelve.open('data/accounts_data.sf',writeback=True) as ad_sf:
        try:
            no_of_accounts = ad_sf['no_of_accounts']
        except KeyError:
            ad_sf['no_of_accounts'] = 0
            no_of_accounts = 0
        n = int(input()) # input number of accounts to be inserted
        i = 0
        while i < n:
            i += 1
            holder_name = fnames[randint(0,len(fnames)-1)] + ' ' + lnames[randint(0,len(lnames)-1)]
            new_acc_no = bank.Account.get_new_acc_no()
            my_acc = bank.Account(new_acc_no,holder_name,randomDate("1/1/2009 12:00 AM", "1/1/2010 12:00 AM", random()))
            no_of_trans = randint(3,10)
            for t in range(no_of_trans):
                amount = randint(5,1000)
                sign = 1
                if random() <= 0.5:
                    sign = -1
                amount *= sign
                my_acc.make_transaction(bank.Transaction(amount,randomDate("1/1/2010 12:00 AM", "1/1/2016 12:00 AM", random())))
            #print(my_acc)
            print(new_acc_no,' ',holder_name)
            ad_sf[str(no_of_accounts+i)] = my_acc
            ad_sf['no_of_accounts'] = no_of_accounts+i
            my_bt.insert_key(new_acc_no,str(no_of_accounts+i))
