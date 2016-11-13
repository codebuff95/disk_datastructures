import bank,shelve,btree

with btree.BTree('data/bank.sf') as my_bt, shelve.open('data/accounts_data.sf',writeback=True) as ad_sf:
    while True:
        req_acc_no = input('Enter account number: ')
        my_key = my_bt.get_key(req_acc_no)
        print('Disk accesses: ',my_key[1])
        print('Tree height: ',my_bt.get_height())
        print('Tree key count: ',my_bt.get_key_count())
        if my_key[0] == None:
            print('Key does not exist!')
            continue
        data_loc = my_key[0][1]
        my_acc = ad_sf[data_loc]
        print('Account details:\n',my_acc)
