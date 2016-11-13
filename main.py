from flask import Flask
import btree,shelve
app = Flask(__name__)
bank_f_n = 'data/bank.sf'
acc_f_n = 'data/accounts_data.sf'
acc_create_log_f_n = 'data/create.log'

@app.route('/search/<acc_no>')
def searcher(acc_no):
    global bank_f_n,acc_f_n,acc_create_log_f_n
    with btree.BTree(bank_f_n) as my_bt, shelve.open(acc_f_n,writeback=True) as ad_sf:
        my_bt_record = my_bt.get_key(acc_no)
        if my_bt_record[0] == None:
            return 'Not found. Disk accesses = ' + str(my_bt_record[1])
        my_acc_dets = ad_sf[my_bt_record[0][1]]
        return str(my_acc_dets)
if __name__ == '__main__':
    app.run(port=8000,host='0.0.0.0',debug=True)
