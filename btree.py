import shelve,mmu,sys
from btree_errors import *
from random import randint
MAX_KEYS = 5
ROOT_PTR = '-1'
NONE_PTR = '-2'
class Node:
    def __init__(self):
        self.keys = []  #a list of tuples, each of format: (key,location)
        self.childs = []
    def __str__(self):
        return 'keys = {}\nchilds = {}'.format(self.keys,self.childs)

    def get_child_ptr(self,index):
        try:
            nex_ptr = self.childs[index]
        except IndexError:
            nex_ptr = NONE_PTR
        return nex_ptr
class BTree:
    def __init__(self,f_name):
        self.f_name = f_name
        self.mmu = mmu.MMU()
    def __enter__(self):
        self.tree = shelve.open(self.f_name,writeback=True)
        return self
    def __exit__(self,*args):
        self.tree.close()
    def get_root(self):
        #root = self.tree[ROOT_PTR]
        root = self.get_node(ROOT_PTR)
        return root

    def get_node(self,ptr):
        """returns a tuple of Node object and the number of disk accesses taken to retrieve the node"""
        if ptr == NONE_PTR:
            return (None,0)
        try:
            retval = self.mmu.retrieve_block(self.tree,ptr)
            return retval
        except KeyError:
            raise NodeNotExistsError

    def get_key(self,requested_key):
        """
            returns a tuple of a tuple of key and the number of disk accesses taken to retrieve the key
            returns None in place of key, if key does not exist.
        """
        (cur_node,local_d_a_c) = self.get_root()
        disk_access_count = 0
        while cur_node != None:
            i = 0
            while i < len(cur_node.keys):
                if requested_key == cur_node.keys[i][0]:
                    return (cur_node.keys[i],disk_access_count)
                elif requested_key < cur_node.keys[i][0]:
                    break
                i += 1

            (cur_node,local_d_a_c) = self.get_node(cur_node.get_child_ptr(i))
            disk_access_count += local_d_a_c
        return (None,disk_access_count) #disk_access_count is returned, even if the key is not found.
    def persist_changes(self,key,value):
        return self.mmu.write_block(self.tree,key,value)

    def get_new_node_ptr(self):
        #return int(self.mmu.retrieve_block(self.tree,NODE_COUNT_PTR)[0]) + 1
        s = ''
        for i in range(16):
            s += str(randint(0,9))
        try:
            self.get_node(s)[0]
            return self.get_new_node_ptr()
        except NodeNotExistsError:
            return s
    def split_root(self):
        old_root = self.get_root()[0]  #old_root will become the 0th child of new_node.
        new_root = Node()   #new_root is the new root of the tree.
        new_child = Node()  #new_child will become the 1st child of new_node.
        new_root.keys.append(old_root.keys[MAX_KEYS//2])
        new_child.keys.extend(old_root.keys[(MAX_KEYS//2)+1:])
        new_child.childs = old_root.childs[(MAX_KEYS//2)+1:]
        old_root.childs = old_root.childs[:(MAX_KEYS//2)+1]
        old_root.keys = old_root.keys[:(MAX_KEYS//2)]
        old_root_ptr = self.get_new_node_ptr()
        new_child_ptr = self.get_new_node_ptr()
        new_root.childs.append(old_root_ptr)
        new_root.childs.append(new_child_ptr)
        self.persist_changes(ROOT_PTR,new_root)
        self.persist_changes(old_root_ptr,old_root)
        self.persist_changes(new_child_ptr,new_child)

    def split_node(self,childptr,parentptr):
        """splits a non-root node."""
        (parent_node,local_d_a_c) = self.get_node(parentptr)
        (child_node,local_d_a_c) = self.get_node(childptr)
        mid_key = child_node.keys[MAX_KEYS//2]
        ins_index = 0
        while ins_index < len(parent_node.keys):
            if mid_key[0] < parent_node.keys[ins_index][0]:
                break
            ins_index += 1

        parent_node.keys.insert(ins_index,mid_key)
        new_node = Node()
        new_node.keys = child_node.keys[(MAX_KEYS//2)+1:]
        new_node.childs = child_node.childs[(MAX_KEYS//2)+1:]
        child_node.keys = child_node.keys[:(MAX_KEYS//2)]
        child_node.childs = child_node.childs[:(MAX_KEYS//2)+1]
        new_node_ptr = self.get_new_node_ptr()
        parent_node.childs.insert(ins_index+1,new_node_ptr)
        self.persist_changes(parentptr,parent_node)
        self.persist_changes(childptr,child_node)
        self.persist_changes(new_node_ptr,new_node)

    def insert_seed(self,key,data):
        try:
            root,local_d_a_c = self.get_root()
            raise TreeAlreadySeededError
        except NodeNotExistsError:
            pass
        new_root = Node()
        new_root.keys.append((key,data))
        self.persist_changes(ROOT_PTR,new_root)
        return 1    #1 disk access done.
    def insert_key(self,key,data):
        #key = key to be inserted, data = data corresponding to the key.
        try:
            (cur_node,local_d_a_c) = self.get_root()
        except NodeNotExistsError:
            return self.insert_seed(key,data)
        (temp_key,disk_access_count) = self.get_key(key)
        if temp_key != None:
            print('key to be inserted already exists in the tree')
            raise KeyExistsError
        cur_node_ptr = ROOT_PTR
        if len(cur_node.keys) >= MAX_KEYS:
            #root is full. split root.
            self.split_root()
            return self.insert_key(key,data)
        
        while len(cur_node.childs) > 0:
            #while cur_node is not a leaf.
            i = 0
            child_node_ptr = None
            while i < len(cur_node.keys):
                if key < cur_node.keys[i][0]:
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
        self._insert_key_in_node(key,data,cur_node_ptr)
        return disk_access_count
    def _insert_key_in_node(self,key,data,nodeptr):
        """Assuming that insertions will take place only in leaf nodes. ie, the node will have an empty childs list"""
        (my_node,local_d_a_c) = self.get_node(nodeptr)
        if len(my_node.childs) > 0:
            """my_node is not a leaf node. cannot insert a key in it."""
            raise NotLeafError
        if len(my_node.keys) >= MAX_KEYS:
            """my_node is already full. cannot insert a key in it."""
            raise NodeFullError
        ins_index = 0
        while ins_index < len(my_node.keys):
            if key < my_node.keys[ins_index][0]:
                break
            ins_index += 1
        my_node.keys.insert(ins_index,tuple((key,data)))
        return self.persist_changes(nodeptr,my_node)
    def _get_key_count(self,nodeptr):
        node = self.get_node(nodeptr)[0]
        k_c = len(node.keys)
        for child in node.childs:
            k_c += self._get_key_count(child)
        return k_c
    def get_key_count(self):
        root = self.get_root()[0]
        k_c = len(root.keys)
        for child in root.childs:
            k_c += self._get_key_count(child)
        return k_c
    def _get_height(self,nodeptr,h_till_now):
        node = self.get_node(nodeptr)[0]
        h = h_till_now
        for childptr in node.childs:
            h = max(h,self._get_height(childptr,h_till_now + 1))
        return h
    def get_height(self):
        root = self.get_root()[0]
        h = 0
        for child in root.childs:
            h = max(h,self._get_height(child,1))
        return h
