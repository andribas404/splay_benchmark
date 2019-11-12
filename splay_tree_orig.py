#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


class Node:
    """Tree Node."""

    def __init__(self, val):
        """Node init."""
        self.val = val
        self.counter = 1
        self._left = None
        self._right = None
        self.parent = None

    @property
    def left(self):
        """Left child."""
        return self._left

    @left.setter
    def left(self, node):
        """Left child setter."""
        self.decrease(self._left)
        self.increase(node)
        self._left = node
        if node:
            node.parent = self

    @property
    def right(self):
        """Right child."""
        return self._right

    @right.setter
    def right(self, node):
        """Right child setter."""
        self.decrease(self._right)
        self.increase(node)
        self._right = node
        if node:
            node.parent = self

    def increase(self, node):
        """Increase counter."""
        if node:
            self.counter += node.counter

    def decrease(self, node):
        """Decrease counter."""
        if node:
            self.counter -= node.counter

    @property
    def is_left(self):
        """Node is left child."""
        return self.parent and self.parent.left == self

    @property
    def is_right(self):
        """Node is right child."""
        return self.parent and self.parent.right == self

    def __repr__(self):
        """Debug representation."""
        return (f"<{self.__class__.__name__}"
                f" val={self.val}, counter={self.counter}>")

    def extract(self):
        self.__init__(self.val)


class SplayTree:
    """
    Splay Tree with implicit index.

    https://neerc.ifmo.ru/wiki/index.php?title=Splay-%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D0%BE

    http://www.cs.cmu.edu/~sleator/papers/self-adjusting.pdf
    """

    def __init__(self):
        """Init tree."""
        self._root = None
        self._step = 0
        self._nodes = []

    def insert(self, x):
        """Insert node."""
        node = Node(x)
        self._nodes.append(node)
        pos = self._add(node)
        return pos

    def remove(self, pos):
        """Remove node."""
        node = self._find_by_pos(pos)
        self._remove(node)

    @property
    def size(self):
        """Size of tree."""
        if self.root:
            return self.root.counter
        return 0

    @property
    def root(self):
        """Tree root."""
        return self._root

    @root.setter
    def root(self, node):
        """Tree root setter."""
        self._root = node
        if self._root:
            self._root.parent = None

    def _splay(self, node):
        """Rotate node."""
        if node is None:
            return
        while node.parent:
            p = node.parent
            if p.parent is None:
                # p is root
                self._zig(node)
                break

            if (p.is_left and node.is_left
            or p.is_right and node.is_right):
                self._zig_zig(node)
            else:
                self._zig_zag(node)
        self.root = node

    def _zig(self, node):
        """Rotate node to root."""
        p = node.parent
        if node.is_left:
            p.left = node.right
            node.right = p
        else:
            p.right = node.left
            node.left = p
        node.parent = None

    def _zig_zig(self, node):
        """Rotate left-left or right-right node."""
        p = node.parent
        g = p.parent

        if node.is_left:
            self.rotate_right(g)
            self.rotate_right(p)
        else:
            self.rotate_left(g)
            self.rotate_left(p)

    def _zig_zag(self, node):
        """Rotate left-right node."""
        p = node.parent
        g = p.parent

        if node.is_left:
            self.rotate_right(p)
            self.rotate_left(g)
        else:
            self.rotate_left(p)
            self.rotate_right(g)

    def _find(self, node):
        """Search node and splay."""
        current = self.root
        while current and current.val != node.val:
            if current.val < node.val:
                current = current.right
            else:
                current = current.left
        self._splay(current)
        return current

    def _find_by_pos(self, pos):
        """Search node by pos and splay."""
        node = self.root
        if not node or pos >= node.counter:
            raise ValueError("Position is out of range")
        while node:
            if node.right:
                if pos < node.right.counter:
                    node = node.right
                    continue
                # skip all right nodes
                pos -= node.right.counter
            if pos == 0:
                break
            # skip this node
            pos -= 1
            node = node.left

        # self._splay(node)
        return node

    def _merge(self, tree):
        """Merge trees."""
        if self.root is None:
            self.root = tree.root
            return
        node = self.most_right
        self._splay(node)
        node.right = tree.root

    def _split(self, val):
        """Split tree."""
        node = self.root
        next_node = None

        left_tree = SplayTree()
        right_tree = SplayTree()

        if node is None:
            return left_tree, right_tree

        while True:
            if node.val > val:
                next_node = node.left
            else:
                next_node = node.right
            if next_node is None:
                break
            node = next_node

        self._splay(node)
        if node.val <= val:
            left_tree.root = node
            right_tree.root = node.right
            node.right = None
        else:
            left_tree.root = node.left
            right_tree.root = node
            node.left = None

        self.root = None
        return left_tree, right_tree

    def _add(self, node):
        """Add node."""
        tree1, tree2 = self._split(node.val)
        self.root = node
        node.left = tree1.root
        node.right = tree2.root
        pos = 0
        if node.right:
            pos = node.right.counter
        return pos

    def _remove(self, node):
        """Remove node."""
        self._splay(node)
        self.root = node.left
        right_tree = SplayTree()
        right_tree.root = node.right
        self._merge(right_tree)
        node.extract()

    @property
    def most_left(self):
        """Most left leaf of tree."""
        size = self.root.counter
        return self._find_by_pos(size - 1)

    @property
    def most_right(self):
        """Most right leaf of tree."""
        return self._find_by_pos(0)

    def rotate_left(self, node):
        """Rotate edge from node to right child counter -clockwise."""
        child = node.right

        counter_node = node.counter
        counter_child = child.counter

        p = node.parent
        if p:
            counter_p = p.counter
            if node.is_left:
                p.left = child
            elif node.is_right:
                p.right = child
            p.counter = counter_p

        child.parent = p

        # child.left, node.right = node, child.left
        grand_child = child.left
        child.left = node
        node.right = grand_child

        node.counter = counter_node - counter_child

        if grand_child:
            node.counter += grand_child.counter
            counter_child -= grand_child.counter

        child.counter = counter_child + node.counter

    def rotate_right(self, node):
        """Rotate edge from node to left child clockwise."""
        child = node.left

        counter_node = node.counter
        counter_child = child.counter

        p = node.parent
        if p:
            counter_p = p.counter
            if node.is_left:
                p.left = child
            elif node.is_right:
                p.right = child
            p.counter = counter_p

        child.parent = p

        # child.right, node.left = node, child.right
        grand_child = child.right
        child.right = node
        node.left = grand_child

        node.counter = counter_node - counter_child

        if grand_child:
            node.counter += grand_child.counter
            counter_child -= grand_child.counter

        child.counter = counter_child + node.counter


class Worker:
    """Worker."""

    def __init__(self):
        """Worker init."""
        self.tree = SplayTree()

    def process(self, commands):
        """Process commands."""
        res = []

        for cmd_code, x in commands:
            if cmd_code == 1:
                pos = self.tree.insert(x)
                res.append(pos)
            elif cmd_code == 2:
                self.tree.remove(x)
            else:
                raise ValueError("Invalid Command")

        return res


if __name__ == "__main__":
    worker = Worker()
    n = int(input())
    commands = []
    for _ in range(n):
        command = list(map(int, input().strip().split()))
        commands.append(command)

    res = worker.process(commands)
    print("\n".join(map(str, res)))
