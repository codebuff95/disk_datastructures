import shelve,mmu,sys

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
class BTree:
    def __init__(self,f_name):
        self.tree = shelve.open(f_name,writeback=True)
        self.mmu = mmu.MMU()
        self.get_root()

    def get_root(self):
        try:
            #root = self.tree[ROOT_PTR]
            root = self.get_node(ROOT_PTR)
            return root
        except KeyError as e:
            print('root does not exist in the provided shelve! aborting the program!')
            sys.exit()

    def get_node(self,ptr):
        """returns a tuple of Node object and the number of disk accesses taken to retrieve the node"""
        if ptr == NONE_PTR:
            return (None,0)
        return self.mmu.retrieve_block(self.tree,ptr)

    def get_key(self,requested_key):
        """returns a tuple of a tuple of key and the number of disk accesses taken to retrieve the key"""
        (cur_node,local_d_a_c) = self.get_root()
        disk_access_count = 0
        while cur_node != None:
            i = 0
            while i < len(cur_node.keys):
                if requested_key == cur_node.keys[i][0]:
                    return (cur_node.keys[i],disk_access_count)
                elif requested_key > cur_node.keys[i][0]:
                    break
                i += 1

            (cur_node,local_d_a_c) = self.get_node(cur_node.get_child_ptr(i))
            disk_access_count += local_d_a_c
        return (None,disk_access_count) #disk_access_count is returned, even if the key is not found.
    def split_node(self,childptr,parentptr):
        (parent_node,local_d_a_c) = self.get_node(parentptr)
        (child_node,local_d_a_c) = self.get_node(childptr)
        mid_key = child_node[MAX_KEYS/2]
        ins_index = 0
        while ins_index < len(parent_node.keys):
            if mid_key > parent_node.keys[ins_index][0]:
                break
            ins_index += 1

        
    def insert_key(self,key,data):
        #key = key to be inserted, data = data to be inserted.
        (key,disk_access_count) = self.get_key(key)
        if key != None:
            print('key to be inserted already exists in the tree')
            raise KeyError('Key already exists')
        (cur_node,local_d_a_c) = self.get_root()
        cur_node_ptr = ROOT_PTR
        while len(cur_node.childs) > 0:
            #while cur_node is not a leaf.
            i = 0
            child_node_ptr = None
            while i < len(cur_node.keys):
                if key > cur_node.keys[i][0]:
                    break
                i += 1
            child_node_ptr = cur_node.get_child_ptr(i)
            child_node,local_d_a_c = self.get_node(child_node_ptr)
            disk_access_count += local_d_a_c
            if len(child_node.keys) >= MAX_KEYS:
                #child_node is full. split child_node.
                self.split_node(childptr=child_node_ptr,parentptr=cur_node_ptr)
                cur_node,local_d_a_c = self.get_node(cur_node_ptr)
                disk_access_count += local_d_a_c
                #run while-loop again for the same cur_node.
                continue
            else:
                #child_node not full. change cur_node to child_node.
                cur_node = child_node
                cur_node_ptr = child_node_ptr
        # cur_node must be the leaf node, insert (key,data) in it.
        self.insert_key_in_node(self,key,data,cur_node_ptr)
        return disk_access_count

if __name__ == '__main__':
    my_btr = BTree('hello')
    my_btr.tree.close()
