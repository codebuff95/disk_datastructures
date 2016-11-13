import account_create,btree
from math import log

bank_f_n = 'data/bank.sf'
ins_n = [0,100,200,300,400,500,600,700,800,900,1000,1500,2000,2500,3000,3500,4000,4500,5000,10000,20000,30000,40000,50000,75000,100000]
if __name__ == '__main__':
    i = 0
    with open('bulk_insert_results.csv','wt',encoding='utf-8') as r_f:
        for i in range(1,len(ins_n)):
            print('i = ',i)
            account_create.start_bulk_creation(ins_n[i] - ins_n[i-1] - 1)
            local_d_a_c = account_create.create_single_account(account_create.generate_random_account())
            with btree.BTree(bank_f_n) as my_bt:
                h = my_bt.get_height()
            r_f.write(str(ins_n[i]) + ',' + str(h) + ',' + str(local_d_a_c) + ',' + str(log(ins_n[i])/log(5)) + '\n')
