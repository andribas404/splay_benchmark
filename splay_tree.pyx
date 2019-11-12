#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3
"""
Splay tree.

7_2. Солдаты Сплей
Ограничение времени	1 секунда
Ограничение памяти	500Mb
Ввод	стандартный ввод или input.txt
Вывод	стандартный вывод или output.txt
В одной военной части решили построить в одну шеренгу по росту.
Т.к. часть была далеко не образцовая, то солдаты часто приходили не вовремя,
а то их и вовсе приходилось выгонять из шеренги за плохо начищенные сапоги.
Однако солдаты в процессе прихода и ухода должны были всегда быть выстроены
по росту – сначала самые высокие, а в конце – самые низкие.
За расстановку солдат отвечал прапорщик, который заметил интересную
особенность – все солдаты в части разного роста.

Ваша задача состоит в том, чтобы помочь прапорщику правильно расставлять
солдат, а именно для каждого приходящего солдата указывать, перед каким
солдатом в строе он должен становится. Требуемая скорость выполнения
команды - O(log n) амортизационно.

В реализации используйте сплей деревья.

Формат ввода
Первая строка содержит число N – количество команд (1 ≤ N ≤ 90 000).

В каждой следующей строке содержится описание команды: число 1 и X если
солдат приходит в строй (X – рост солдата, натуральное число до 100 000
включительно) и число 2 и Y если солдата, стоящим в строе на месте Y надо
удалить из строя. Солдаты в строе нумеруются с нуля.

Формат вывода
На каждую команду 1 (добавление в строй) вы должны выводить
число K – номер позиции, на которую должен встать этот солдат
(все стоящие за ним двигаются назад).
"""

cdef class Node:
    """Tree Node."""
    cdef int val
    cdef int counter
    cdef Node _left
    cdef Node _right
    cdef Node parent

    def __init__(self, int val):
        """Node init."""
        self.val = val
        self.counter = 1
        self._left = None
        self._right = None
        self.parent = None

    cdef Node get_left(self):
        """Left child."""
        return self._left

    cdef void set_left(self, Node node):
        """Left child setter."""
        self.decrease(self.get_left())
        self.increase(node)
        self._left = node
        if node:
            node.parent = self

    cdef Node get_right(self):
        """Right child."""
        return self._right

    cdef void set_right(self, Node node):
        """Right child setter."""
        self.decrease(self.get_right())
        self.increase(node)
        self._right = node
        if node:
            node.parent = self

    cdef void increase(self, Node node):
        """Increase counter."""
        if node:
            self.counter += node.counter

    cdef void decrease(self, Node node):
        """Decrease counter."""
        if node:
            self.counter -= node.counter

    cdef bint is_left(self):
        """Node is left child."""
        return self.parent and self.parent.get_left() == self

    cdef bint is_right(self):
        """Node is right child."""
        return self.parent and self.parent.get_right() == self

    cdef void extract(self):
        self.__init__(self.val)


cdef class SplayTree:
    """Splay Tree.

    https://neerc.ifmo.ru/wiki/index.php?title=Splay-%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D0%BE

    http://www.cs.cmu.edu/~sleator/papers/self-adjusting.pdf
    """
    cdef Node _root
    cdef int _step

    def __init__(self):
        """Init tree."""
        self._root = None
        self._step = 0

    cpdef int insert(self, int x):
        """Insert node."""
        node = Node(x)
        pos = self._add(node)
        return pos

    cpdef void remove(self, int pos):
        """Remove node."""
        node = self._find_by_pos(pos)
        self._remove(node)

    cdef int get_size(self):
        """Size of tree."""
        if self.get_root():
            return self.get_root().counter
        return 0

    cdef Node get_root(self):
        """Tree root."""
        return self._root

    cdef void set_root(self, Node node):
        """Tree root setter."""
        self._root = node
        if self._root:
            self._root.parent = None

    cdef void _splay(self, Node node):
        """Rotate node."""
        if node is None:
            return
        while node.parent:
            p = node.parent
            if p.parent is None:
                # p is root
                self._zig(node)
                break

            if (p.is_left() and node.is_left()
            or p.is_right() and node.is_right()):
                self._zig_zig(node)
            else:
                self._zig_zag(node)
        self.set_root(node)

    cdef void _zig(self, Node node):
        """Rotate node to root."""
        p = node.parent
        if node.is_left():
            p.set_left(node.get_right())
            node.set_right(p)
        else:
            p.set_right(node.get_left())
            node.set_left(p)
        node.parent = None

    cdef void _zig_zig(self, Node node):
        """Rotate left-left or right-right node."""
        p = node.parent
        g = p.parent

        if node.is_left():
            self.rotate_right(g)
            self.rotate_right(p)
        else:
            self.rotate_left(g)
            self.rotate_left(p)

    cdef void _zig_zag(self, Node node):
        """Rotate left-right node."""
        p = node.parent
        g = p.parent

        if node.is_left():
            self.rotate_right(p)
            self.rotate_left(g)
        else:
            self.rotate_left(p)
            self.rotate_right(g)

    cdef Node _find(self, Node node):
        """Search node and splay."""
        cdef Node current = self.get_root()
        while current and current.val != node.val:
            if current.val < node.val:
                current = current.get_right()
            else:
                current = current.get_left()
        self._splay(current)
        return current

    cdef Node _find_by_pos(self, int pos):
        """Search node by pos and splay."""
        cdef Node node = self.get_root()
        if not node or pos >= node.counter:
            raise ValueError("Position is out of range")
        while node:
            if node.get_right():
                if pos < node.get_right().counter:
                    node = node.get_right()
                    continue
                # skip all right nodes
                pos -= node.get_right().counter
            if pos == 0:
                break
            # skip this node
            pos -= 1
            node = node.get_left()

        # self._splay(node)
        return node

    cdef void _merge(self, SplayTree tree):
        """Merge trees."""
        if self.get_root() is None:
            self.set_root(tree.get_root())
            return
        node = self.most_right()
        self._splay(node)
        node.set_right(tree.get_root())

    # Tuple types can't (yet) contain Python objects.
    cdef void _split(self, int val, SplayTree left_tree, SplayTree right_tree):
        """Split tree."""
        node = self.get_root()
        next_node = None

        if node is None:
            return

        while True:
            if node.val > val:
                next_node = node.get_left()
            else:
                next_node = node.get_right()
            if next_node is None:
                break
            node = next_node

        self._splay(node)
        if node.val <= val:
            left_tree.set_root(node)
            right_tree.set_root(node.get_right())
            node.set_right(None)
        else:
            left_tree.set_root(node.get_left())
            right_tree.set_root(node)
            node.set_left(None)

        self.set_root(None)

    cdef int _add(self, Node node):
        """Add node."""
        cdef SplayTree tree1 = SplayTree()
        cdef SplayTree tree2 = SplayTree()


        self._split(node.val, tree1, tree2)
        self.set_root(node)
        node.set_left(tree1.get_root())
        node.set_right(tree2.get_root())
        pos = 0
        if node.get_right():
            pos = node.get_right().counter
        return pos

    cdef void _remove(self, Node node):
        """Remove node."""
        self._splay(node)
        self.set_root(node.get_left())
        right_tree = SplayTree()
        right_tree.set_root(node.get_right())
        self._merge(right_tree)
        node.extract()

    cdef Node most_left(self):
        """Most left leaf of tree."""
        cdef int size = self.get_root().counter
        return self._find_by_pos(size - 1)

    cdef Node most_right(self):
        """Most right leaf of tree."""
        return self._find_by_pos(0)

    cdef void rotate_left(self, Node node):
        """Rotate edge from node to right child counter -clockwise."""
        cdef Node child = node.get_right()

        cdef int counter_node = node.counter
        cdef int counter_child = child.counter

        cdef Node p = node.parent
        if p:
            counter_p = p.counter
            if node.is_left():
                p.set_left(child)
            elif node.is_right():
                p.set_right(child)
            p.counter = counter_p

        child.parent = p

        cdef Node grand_child = child.get_left()
        child.set_left(node)
        node.set_right(grand_child)

        node.counter = counter_node - counter_child

        if grand_child:
            node.counter += grand_child.counter
            counter_child -= grand_child.counter

        child.counter = counter_child + node.counter

    cdef void rotate_right(self, Node node):
        """Rotate edge from node to left child clockwise."""
        cdef Node child = node.get_left()

        cdef int counter_node = node.counter
        cdef int counter_child = child.counter

        cdef Node p = node.parent
        if p:
            counter_p = p.counter
            if node.is_left():
                p.set_left(child)
            elif node.is_right():
                p.set_right(child)
            p.counter = counter_p

        child.parent = p

        cdef Node grand_child = child.get_right()
        child.set_right(node)
        node.set_left(grand_child)

        node.counter = counter_node - counter_child

        if grand_child:
            node.counter += grand_child.counter
            counter_child -= grand_child.counter

        child.counter = counter_child + node.counter
