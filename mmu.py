"""The module for the Memory Management Unit used in this project"""
import shelve
class MMU:
    def __init__(self):
        self.frames = []
        self.max_frames = 8
    def retrieve_block(self,my_btree,btree_ptr):#my_btree is a shelve.
        """returns a tuple of Node object and the number of disk accesses taken to retrieve the object"""
        if self.frames.count(btree_ptr) > 0:
            #the block is already present in the frames.
            return (my_btree[btree_ptr],0)
        else:
            #the block is not already present in the frames.
            self.frames.append(btree_ptr)
            if len(self.frames) > 8:
                self.frames = self.frames[1:]
            return (my_btree[btree_ptr],1)
