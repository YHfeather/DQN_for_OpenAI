import numpy as np
class SumTree(object):
    '''
    定义DQN中的Memory存储结构 SumTree
    这里使用一个np.array表示整棵树
    '''
    data_pointer = 0
    def __init__(self, capacity):
        self.capacity = capacity
        self.tree = np.zeros(2 * capacity - 1)
        self.data = np.zeros(capacity, dtype=object)


    def add(self, p, data):
        '''
        将新的记忆添加到tree中
        :param p:
        :param data:
        :return:
        '''
        tree_idx = self.data_pointer + self.capacity - 1
        self.data[self.data_pointer] = data
        self.update(tree_idx, p)

        self.data_pointer += 1
        if self.data_pointer >= self.capacity:
            self.data_pointer = 0

    def update(self, tree_idx, p):
        '''
        当一个记忆数据被用来训练时，会产生新的优先值p，根据新的p值更新树
        :param tree_idx:
        :param p:
        :return:
        '''
        change = p - self.tree[tree_idx]
        self.tree[tree_idx] = p
        while tree_idx != 0:
            tree_idx = (tree_idx - 1) // 2
            self.tree[tree_idx] += change

    def get_leaf(self, v):
        '''
        根据选取的v进行抽样
        :param v:
        :return:
        '''
        parent_idx = 0
        while True:
            cl_idx = 2 * parent_idx + 1
            cr_idx = cl_idx + 1
            if cl_idx >= len(self.tree):
                leaf_idx = parent_idx
                break
            else:
                if v <= self.tree[cl_idx]:
                    parent_idx = cl_idx
                else:
                    v -= self.tree[cl_idx]
                    parent_idx = cr_idx

        data_idx = leaf_idx - self.capacity + 1
        return leaf_idx, self.tree[leaf_idx], self.data[data_idx]

    @property
    def total_p(self):
        '''
        获取全部优先级的和（根节点的值）
        :return:
        '''
        return self.tree[0]