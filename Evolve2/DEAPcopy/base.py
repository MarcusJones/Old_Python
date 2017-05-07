#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

"""The :mod:`~deap.base` module provides basic structures to build evolutionary
algorithms. It contains only two simple containers that are a basic N-ary 
:class:`~deap.base.Tree`, usefull for implementing genetic programing, and a 
virtual :class:`~deap.base.Fitness` class used as base class, for the fitness 
member of any individual.
"""

import sys
import copy
import operator
import functools

from collections import deque, Sequence
from itertools import izip, repeat, count

class Toolbox(object):
    """A toolbox for evolution that contains the evolutionary operators.
    At first the toolbox contains two simple methods. The first method
    :meth:`~deap.toolbox.clone` duplicates any element it is passed as
    argument, this method defaults to the :func:`copy.deepcopy` function.
    The second method :meth:`~deap.toolbox.map` applies the function given
    as first argument to every items of the iterables given as next
    arguments, this method defaults to the :func:`map` function. You may
    populate the toolbox with any other function by using the
    :meth:`~deap.base.Toolbox.register` method.
    """

    def __init__(self):
        self.register("clone", copy.deepcopy)
        self.register("map", map)

    def register(self, alias, method, *args, **kargs):
        """Register a *method* in the toolbox under the name *alias*. You 
        may provide default arguments that will be passed automatically when 
        calling the registered method. Fixed arguments can then be overriden 
        at function call time.
        
        :param alias: The name the operator will take in the toolbox. If the
                      alias already exist it will overwrite the the operator
                      already present.
        :param method: The function to which refer the alias.
        :param argument: One or more argument (and keyword argument) to pass
                         automatically to the registered function when called,
                         optional.
        
        The following code block is an example of how the toolbox is used. ::

            >>> def func(a, b, c=3):
            ...     print a, b, c
            ... 
            >>> tools = Toolbox()
            >>> tools.register("myFunc", func, 2, c=4)
            >>> tools.myFunc(3)
            2 3 4
        
        The registered function will be given the attributes :attr:`__name__`
        set to the alias and :attr:`__doc__` set to the original function's
        documentation. The :attr:`__dict__` attribute will also be updated
        with the original function's instance dictionnary, if any.
        """
        pfunc = functools.partial(method, *args, **kargs)
        pfunc.__name__ = alias
        pfunc.__doc__ = method.__doc__
        
        try:
            # Some methods don't have any dictionary, in these cases simply 
            # don't copy it.
            pfunc.__dict__.update(method.__dict__.copy())
        except AttributeError:
            pass
        
        setattr(self, alias, pfunc)

    def unregister(self, alias):
        """Unregister *alias* from the toolbox.
        
        :param alias: The name of the operator to remove from the toolbox.
        """
        delattr(self, alias)

    def decorate(self, alias, *decorators):
        """Decorate *alias* with the specified *decorators*, *alias*
        has to be a registered function in the current toolbox.
        
        :param alias: The name of the operator to decorate.
        :param decorator: One or more function decorator. If multiple
                          decorators are provided they will be applied in
                          order, with the last decorator decorating all the
                          others.
        
        .. versionchanged:: 0.8
           Decoration is not signature preserving anymore.
        """
        pfunc = getattr(self, alias)
        method, args, kargs = pfunc.func, pfunc.args, pfunc.keywords
        for decorator in decorators:
            method = decorator(method)
        self.register(alias, method, *args, **kargs)

class Fitness(object):
    """The fitness is a measure of quality of a solution. If *values* are
    provided as a tuple, the fitness is initalized using those values,
    otherwise it is empty (or invalid).
    
    :param values: The initial values of the fitness as a tuple, optional.

    Fitnesses may be compared using the ``>``, ``<``, ``>=``, ``<=``, ``==``,
    ``!=``. The comparison of those operators is made lexicographically.
    Maximization and minimization are taken care off by a multiplication
    between the :attr:`weights` and the fitness :attr:`values`. The comparison
    can be made between fitnesses of different size, if the fitnesses are
    equal until the extra elements, the longer fitness will be superior to the
    shorter.

    .. note::
       When comparing fitness values that are **minimized**, ``a > b`` will
       return :data:`True` if *a* is **smaller** than *b*.
    """
    
    weights = None
    """The weights are used in the fitness comparison. They are shared among
    all fitnesses of the same type. When subclassing :class:`Fitness`, the
    weights must be defined as a tuple where each element is associated to an
    objective. A negative weight element corresponds to the minimization of
    the associated objective and positive weight to the maximization.

    .. note::
        If weights is not defined during subclassing, the following error will 
        occur at instantiation of a subclass fitness object: 
        
        ``TypeError: Can't instantiate abstract <class Fitness[...]> with
        abstract attribute weights.``
    """
    
    wvalues = ()
    """Contains the weighted values of the fitness, the multiplication with the
    weights is made when the values are set via the property :attr:`values`.
    Multiplication is made on setting of the values for efficiency.
    
    Generally it is unnecessary to manipulate wvalues as it is an internal
    attribute of the fitness used in the comparison operators.
    """
    
    def __init__(self, values=()):
        if self.weights is None:
            raise TypeError("Can't instantiate abstract %r with abstract "
                "attribute weights." % (self.__class__))
        
        if not isinstance(self.weights, Sequence):
            raise TypeError("Attribute weights of %r must be a sequence." 
                % self.__class__)
        
        if len(values) > 0:
            self.values = values
        
    def getValues(self):
        return tuple(map(operator.truediv, self.wvalues, self.weights))
            
    def setValues(self, values):
        try:
            self.wvalues = tuple(map(operator.mul, values, self.weights))
        except TypeError:
            _, _, traceback = sys.exc_info()
            raise TypeError, ("Both weights and assigned values must be a "
            "sequence of numbers when assigning to values of "
            "%r." % self.__class__, ), traceback
            
    def delValues(self):
        self.wvalues = ()

    values = property(getValues, setValues, delValues,
        ("Fitness values. Use directly ``individual.fitness.values = values`` "
         "in order to set the fitness and ``del individual.fitness.values`` "
         "in order to clear (invalidate) the fitness. The (unweighted) fitness "
         "can be directly accessed via ``individual.fitness.values``."))
    
    @property 
    def valid(self):
        """Assess if a fitness is valid or not."""
        return len(self.wvalues) != 0
        
    def __gt__(self, other):
        return not self.__le__(other)
        
    def __ge__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        if not other:                   # Protection against yamling
            return False
        return self.wvalues <= other.wvalues

    def __lt__(self, other):
        if not other:                   # Protection against yamling
            return False
        return self.wvalues < other.wvalues

    def __eq__(self, other):
        if not other:                   # Protection against yamling
            return False
        return self.wvalues == other.wvalues
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def __deepcopy__(self, memo):
        """Replace the basic deepcopy function with a faster one.
        
        It assumes that the elements in the :attr:`values` tuple are 
        immutable and the fitness does not contain any other object 
        than :attr:`values` and :attr:`weights`.
        """
        copy = self.__class__()
        copy.wvalues = self.wvalues
        return copy

    def __str__(self):
        """Return the values of the Fitness object."""
        return str(self.values)

    def __repr__(self):
        """Return the Python code to build a copy of the object."""
        module = self.__module__
        name = self.__class__.__name__
        return "%s.%s(%r)" % (module, name, self.values)

class Tree(list):
    """Basic N-ary tree class. A tree is initialized from the list `content`.
    The first element of the list is the root of the tree, then the
    following elements are the nodes. Each node can be either a list or a 
    single element. In the case of a list, it is considered as a subtree, 
    otherwise a leaf.
    """
    
    class NodeProxy(object):
        __slots__ = ['obj']
        def __new__(cls, obj, *args, **kargs):
            if isinstance(obj, cls):
                return obj
            inst = object.__new__(cls)
            inst.obj = obj
            return inst
            
        def getstate(self):
            """Return the state of the NodeProxy: the proxied object."""
            return self.obj
            
        @property
        def size(self):
            """Return the size of a leaf: 1."""
            return 1
            
        @property
        def height(self):
            """Return the height of a leaf: 0."""
            return 0
            
        @property
        def root(self):
            """Return the root of a leaf: itself."""
            return self
        
        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return self.obj == other.obj
            else:
                return False

        def __getattr__(self, attr):
            return getattr(self.obj, attr)
        def __call__(self, *args, **kargs):
            return self.obj(*args, **kargs)
        def __repr__(self):
            return self.obj.__repr__()
        def __str__(self):
            return self.obj.__str__()
                
    @classmethod        
    def convertNode(cls, node):
        """Convert node into the proper object either a Tree or a Node."""
        if isinstance(node, cls):
            if len(node) == 1:
                return cls.NodeProxy(node[0])
            return node
        elif isinstance(node, list):
            if len(node) > 1:
                return cls(node)
            else:
                return cls.NodeProxy(node[0])
        else:
            return cls.NodeProxy(node)

    def __init__(self, content=None):
        """Initialize a tree with a list `content`.
        
        The first element of the list is the root of the tree, then the
        following elements are the nodes. A node could be a list, then
        representing a subtree.
        """
        for elem in content:
            self.append(self.convertNode(elem))
        
    def getstate(self):
        """Return the state of the Tree as a list of arbitrary elements.
        It is mainly used for pickling a Tree object.
        """
        return [elem.getstate() for elem in self] 
    
    def __reduce__(self):
        """Return the class init, the object's state and the object's
        dict in a tuple. The function is used to pickle Tree.
        """
        return (self.__class__, (self.getstate(),), self.__dict__)
    
    def __deepcopy__(self, memo):
        """Deepcopy a Tree by first converting it back to a list of list."""
        new = self.__class__(copy.deepcopy(self.getstate()))
        new.__dict__.update(copy.deepcopy(self.__dict__, memo))
        return new
        
    def __setitem__(self, key, value):
        """Set the item at `key` with the corresponding `value`."""
        list.__setitem__(self, key, self.convertNode(value))
        
    def __setslice__(self, i, j, value):
        """Set the slice at `i` to `j` with the corresponding `value`."""
        list.__setslice__(self, i, j, self.convertNode(value))
            
    def __str__(self):
        """Return the tree in its original form, a list, as a string."""
        return list.__str__(self)
        
    def __repr__(self):
        """Return the Python code to build a copy of the object."""
        module = self.__module__
        name = self.__class__.__name__
        return "%s.%s(%s)" % (module, name, list.__repr__(self))
        
    @property
    def root(self):
        """Return the root element of the tree.
        
        The root node of a tree is the node with no parents. There is at most 
        one root node in a rooted tree.
        """
        return self[0]

    @property
    def size(self):
        """Return the number of nodes in the tree.
        
        The size of a node is the number of descendants it has including itself.
        """
        return sum(elem.size for elem in self)

    @property
    def height(self):
        """Return the height of the tree.
        
        The height of a tree is the length of the path from the root to the 
        deepest node in the tree. A (rooted) tree with only one node (the root) 
        has a height of zero.
        """
        try:
            return max(elem.height for elem in self[1:])+1
        except ValueError:
            return 0
    
    @property
    def iter(self):
        """Return a generator function that iterates on the element
         of the tree in linear time using depth first algorithm.
        
            >>> t = Tree([1,2,3[4,5,[6,7]],8])
            >>> [i for i in t.iter]:
            [1, 2, 3, 4, 5, 6, 7, 8]
        """
        for elem in self:
            if isinstance(elem, Tree):
                for elem2 in elem.iter:
                    yield elem2
            else:
                yield elem
    
    @property
    def iter_leaf(self):
        """Return a generator function that iterates on the leaf
         of the tree in linear time using depth first 
         algorithm.
    
            >>> t = Tree([1,2,3,[4,5,[6,7]],8])
            >>> [i for i in t.iter_leaf]
            [2, 3, 5, 7, 8]
        """
        for elem in self[1:]:
            if isinstance(elem, Tree):
                for elem2 in elem.iter_leaf:
                    yield elem2
            else:
                yield elem
    
    @property
    def iter_leaf_idx(self):
        """Return a generator function that iterates on the leaf
        indices of the tree in linear time using depth first 
        algorithm.
        
            >>>  t = Tree([1,2,3,[4,[5,6,7],[8,9]],[10,11]]);
            >>> [i for i in t.iter_leaf_idx]
            [1, 2, 5, 6, 8, 10]
        """
        def leaf_idx(tree, total):
            total[0] += 1
            for elem in tree[1:]:
                if isinstance(elem, Tree):
                    for elem2 in leaf_idx(elem, total):
                        yield total[0]
                else:
                    yield total[0]
                    total[0] += 1
        return leaf_idx(self, [0])

    def searchSubtreeDF(self, index):
        """Search the subtree with the corresponding index based on a 
        depth-first search.
        """
        if index == 0:
            return self
        total = 0
        for child in self:
            if total == index:
                return child
            nbr_child = child.size
            if nbr_child + total > index:
                return child.searchSubtreeDF(index-total)
            total += nbr_child

    def setSubtreeDF(self, index, subtree):
        """Replace the tree with the corresponding index by subtree based
        on a depth-first search.
        """
        if index == 0:
            try:
                self[:] = subtree
            except TypeError:
                del self[1:]
                self[0] = subtree
            return
    
        total = 0
        for i, child in enumerate(self):
            if total == index:
                self[i] = subtree
                return
            nbr_child = child.size
            if nbr_child + total > index:
                child.setSubtreeDF(index-total, subtree)
                return
            total += nbr_child

    def searchSubtreeBF(self, index):
        """Search the subtree with the corresponding index based on a 
        breadth-first search.
        """
        if index == 0:
            return self
        queue = deque(self[1:])
        for i in xrange(index):
            subtree = queue.popleft()
            if isinstance(subtree, Tree):
                queue.extend(subtree[1:])
        return subtree

    def setSubtreeBF(self, index, subtree):
        """Replace the subtree with the corresponding index by subtree based
        on a breadth-first search.
        """
        if index == 0:
            try:
                self[:] = subtree
            except TypeError:
                del self[1:]
                self[0] = subtree
            return
         
        queue = deque(izip(repeat(self, len(self[1:])), count(1)))
        for i in xrange(index):
            elem = queue.popleft()
            parent = elem[0]
            child  = elem[1]
            if isinstance(parent[child], Tree):
                tree = parent[child]
                queue.extend(izip(repeat(tree, len(tree[1:])), count(1)))
        parent[child] = subtree
