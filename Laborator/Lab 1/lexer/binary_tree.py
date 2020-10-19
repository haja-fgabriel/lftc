# TODO finish implementation of binary tree

from colorama import *

class Data:
    def __init__(self, value, _id):
        self.__value__ = value
        self.__id__ = _id

    def get_value(self): return self.__value__
    def set_value(self, new_val): self.__value__ = new_val

    def get_id(self): return self.__id__
    def set_id(self, new_id): self.__id__ = new_val

    value = property(get_value, set_value)
    _id = property(get_id, set_id)

class Identifier(Data):
    def __init__(self, value, _id):
        super().__init__(value, _id)

class Constant(Data):
    def __init__(self, args):
        super().__init__(value, _id)



class Node:
    def __init__(self, data):
        #self.value
        #self.id
        #self.type
        self.data = data
        self.height = 1
        self.left_son = None
        self.right_son = None
    


class BinaryTree:
    def __init__(self):
        self.__count = 0
        self.__root = None
        pass

    def add(self, val, node = None, parent = None):
        # node = self.__root if node is None else node
        # print(f"After: {node}")
        # print(val)
        ret_val = None
        if node is None:
            if parent is None:
                if self.__root is None:
                    self.__count += 1
                    data = Data(val, self.__count)
                    node = Node(data)
                    self.__root = node
                    return node.data.value, node.data._id
                else:
                    node = self.__root
            else:
                self.__count += 1
                data = Data(val, self.__count)
                node = Node(data)
                if parent.data.value > val:
                    parent.left_son = node
                else:
                    parent.right_son = node
                return node.data.value, node.data._id
            #TODO decide on the node parameters
        
        if node.data.value > val:
            ret_val = self.add(val, node=node.left_son, parent=node)
        elif node.data.value < val:
            ret_val = self.add(val, node=node.right_son, parent=node)
        else:
            return node.data.value, node.data._id
        
        # self.__balance(node, parent)
        self.__set_height(node)
        return ret_val[0], ret_val[1]

    def remove(self, val):
        pass
    
    def search(self, val):
        node = self.__root
        while node is not None:
            if val == node.data.value:
                return node.data.value, node.data._id
            elif val < node.data.value:
                node = node.left_son
            else:
                node = node.right_son

        return None, None
    
    def __set_height(self, node):
        left_h = 0 if node.left_son is None else node.left_son.height
        right_h = 0 if node.right_son is None else node.right_son.height
        node.height = max(left_h, right_h) + 1

    def __balance_factor(self, node):
        left_h = 0 if node.left_son is None else node.left_son.height
        right_h = 0 if node.right_son is None else node.right_son.height
        return right_h - left_h


    # TODO check balancing again
    def __balance(self, node, parent):
        bf = self.__balance_factor(node)
        if bf < -1:
            left_bf = self.__balance_factor(node.left_son)
            if left_bf > 1:
                self.__left_rotation(node.left_son, parent)
            self.__right_rotation(node, parent)
        elif bf > 1:
            right_bf = self.__balance_factor(node.right_son)
            if right_bf < -1:
                self.__right_rotation(node.right_son, parent)
            self.__left_rotation(node, parent)

    # TODO check how can you change the link from its parent
    # TODO check for null sons
    def __left_rotation(self, node, parent):
        r_son = node.right_son
        rl_son = r_son.left_son
        node.right_son = rl_son
        r_son.left_son = node
        if node == self.__root:
            root = r_son
        else:
            if parent.left_son == node:
                parent.left_son = r_son
            else:
                parent.right_son = r_son
        self.__set_height(node)
        self.__set_height(r_son)
        
    def __right_rotation(self, node, parent):
        l_son = node.left_son
        lr_son = l_son.right_son
        node.left_son = lr_son
        l_son.right_son = node
        if node == self.__root:
            root = l_son
        else:
            if parent.left_son == node:
                parent.left_son = l_son
            else:
                parent.right_son = l_son
        self.__set_height(node)
        self.__set_height(l_son)

    def __get__all(self, node):
        if node is None: return []
        result = self.__get__all(node.left_son)
        result += [(node.data._id, node.data.value)]
        return result + self.__get__all(node.right_son)
    
    def get_all(self):
        return self.__get__all(self.__root)

    def print_elems(self, id_col, val_col):
        print(Fore.YELLOW + f"    {id_col:20} {val_col:20}")
        for elem in sorted(self.get_all(), key=lambda t:t[0]):
            #print(elem)
            print(Fore.GREEN + f"    {elem[0]:<20} {elem[1]:20}")


if __name__ == '__main__':
    t = BinaryTree()
    t.add('asd')
    t.add('dsa')
    ans = t.search('asd')
    assert(ans is not None and ans.value == 'asd')