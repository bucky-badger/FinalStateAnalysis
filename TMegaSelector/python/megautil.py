'''

Tool for building tree selection functors using syntactic sugar.

Author: Evan K. Friis, UW Madison

The MetaTree object can be used to construct arbitrary cuts strings.

>>> tree = MetaTree()
>>> tree.muPt
Branch('muPt')
>>> mu_cut = tree.muPt > 20.0

Cut is a function that takes a TTree as the argument

>>> mu_cut.__doc__
'branch[muPt] > 20.0'


Make a fake tree:

>>> class Empty:
...    pass
>>> fake_tree = Empty()
>>> fake_tree.muPt = 25
>>> fake_tree.elecPt = 20

>>> mu_cut(fake_tree)
True
>>> mu_cut = tree.muPt < 20
>>> mu_cut(fake_tree)
False

You can do two-branch operations:

>>> mu_is_harder = tree.muPt > tree.elecPt
>>> mu_is_harder(fake_tree)
True
>>> fake_tree.elecPt = 50
>>> mu_is_harder(fake_tree)
False

The MetaTree object also keeps track of which branches are accessed:

>>> tree.active_branches()
['elecPt', 'muPt']

'''


import operator

_operator_names = {
    operator.lt : '<',
    operator.gt : '>',
    operator.ge : '>=',
    operator.le : '<=',
}

def _two_branch_op(b1, b2, op):
    def functor(tree):
        return op(getattr(tree, b1), getattr(tree, b2))
    functor.__doc__ = "branch[%s] %s branch[%s]" % (b1, _operator_names[op], b2)
    return functor

def _one_branch_op(b1, val, op):
    def functor(tree):
        return op(getattr(tree, b1), val)
    functor.__doc__ = "branch[%s] %s %s" % (b1, _operator_names[op], val)
    return functor

class Branch(object):
    def __init__(self, branch):
        self.branch = branch

    def handle_op(self, other, the_op):
        if isinstance(other, Branch):
            return _two_branch_op(self.branch, other.branch, the_op)
        else:
            return _one_branch_op(self.branch, other, the_op)

    def __lt__(self, other):
        return self.handle_op(other, operator.lt)

    def __le__(self, other):
        return self.handle_op(other, operator.le)

    def __ge__(self, other):
        return self.handle_op(other, operator.ge)

    def __gt__(self, other):
        return self.handle_op(other, operator.gt)

    def __repr__(self):
        return "Branch('%s')" % self.branch

class MetaTree(object):
    def __init__(self):
        self.touched_branches = set([])

    def active_branches(self):
        return sorted(self.touched_branches)

    def __getattr__(self, attr):
        self.touched_branches.add(attr)
        return Branch(attr)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
