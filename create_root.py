#create root.
import shelve,os
MAX_KEYS = 5
ROOT_PTR = '-1'
NONE_PTR = '-2'
NODE_COUNT_PTR = '-3'
class Node:
    def __init__(self):
        self.keys = []  #a list of tuples, each of format: (key,location)
        self.childs = []
    def get_child_ptr(self,index):
        try:
            nex_ptr = self.childs[index]
        except IndexError:
            nex_ptr = NONE_PTR
        return nex_ptr

if __name__ == '__main__':
    my_root = Node()
    my_root.keys.append(tuple(('acc0','loc0')))
    os.remove('hello')
    my_btr = shelve.open('hello',writeback=True)
    my_btr[ROOT_PTR] = my_root
    my_btr[NODE_COUNT_PTR] = 0
    my_btr.close()
