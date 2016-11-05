#create root.
import shelve
MAX_KEYS = 5
ROOT_PTR = '-1'
NONE_PTR = '-2'
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
    my_root.keys.append(tuple(('abcdefgh','locate12')))
    my_btr = shelve.open('hello')
    my_btr[ROOT_PTR] = my_root
    my_btr.close()
