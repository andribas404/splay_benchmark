/*
Copyright 2019 Andrey Petukhov

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
*/

#include <iostream>
#include <tuple>
#include <vector>

using std::vector;

namespace splay_tree {
class Node;
class SplayTree;
};

using splay_tree::Node;
using splay_tree::SplayTree;

typedef std::tuple<SplayTree*, SplayTree*> myTuple;
typedef std::tuple<int, int> myCmd;

class Node {
    // """Tree Node."""
 private:
    Node* _left;
    Node* _right;
    Node* parent;
    int counter;
    int val;

 public:
    explicit Node(int val) :
    val(val)  {
        // """Node init."""
        counter = 1;
        _left = nullptr;
        _right = nullptr;
        parent = nullptr;
    }
    int get_val() {
        // """Get value."""
        return val;
    }
    int get_counter() {
        // """Get counter."""
        return counter;
    }
    void set_counter(int c) {
        // """Set counter."""
        counter = c;
    }
    Node* get_parent() {
        // """Get parent."""
        return parent;
    }
    void set_parent(Node* p) {
        // """Set parent."""
        parent = p;
    }
    // @property
    Node* get_left() {
        // """Left child."""
        return _left;
    }
    // @left.setter
    void set_left(Node* node) {
        // """Left child setter."""
        decrease(_left);
        increase(node);
        _left = node;
        if (node) {
            node->parent = this;
        }
    }
    // @property
    Node* get_right() {
        // """Right child."""
        return _right;
    }
    // @right.setter
    void set_right(Node* node) {
        // """Right child setter."""
        decrease(_right);
        increase(node);
        _right = node;
        if (node) {
            node->parent = this;
        }
    }
    // @property
    bool is_left() {
        // """Node is left child."""
        return parent && parent->get_left() == this;
    }
    // @property
    bool is_right() {
        // """Node is right child."""
        return parent && parent->get_right() == this;
    }

 protected:
    void increase(Node* node) {
        // """Increase counter."""
        if (node) {
            counter += node->counter;
        }
    }
    void decrease(Node* node) {
        // """Decrease counter."""
        if (node) {
            counter -= node->counter;
        }
    }
};

class SplayTree {
    /* """Splay Tree.

    https://neerc.ifmo.ru/wiki/index.php?title=Splay-%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D0%BE

    http://www.cs.cmu.edu/~sleator/papers/self-adjusting.pdf
    """*/
 private:
    Node* _root;
    vector<Node*> nodes;

 public:
    SplayTree() {
        // """Init tree."""
        _root = nullptr;
    }
    ~SplayTree() {
        // """Init tree."""
        for (auto it = nodes.begin(); it != nodes.end(); it++) {
            delete *it;
        }
    }
    int insert(int x) {
        // """Insert node."""
        Node* node = new Node(x);
        nodes.push_back(node);
        int pos = _add(node);
        return pos;
    }
    void remove(int pos) {
        // """Remove node."""
        Node* node = _find_by_pos(pos);
        _remove(node);
    }
    // @property
    int get_size() {
        // """Size of tree."""
        if (get_root()) {
            return get_root()->get_counter();
        }
        return 0;
    }

 protected:
    // @property
    Node* get_root() {
        // """Tree root."""
        return _root;
    }
    // @root.setter
    void set_root(Node* node) {
        // """Tree root setter."""
        _root = node;
        if (_root) {
            _root->set_parent(nullptr);
        }
    }
    void _splay(Node* node) {
        // """Rotate node."""
        if (!node) {
            return;
        }
        while (node->get_parent()) {
            Node* p = node->get_parent();
            if (!p->get_parent()) {
                // # p is root
                _zig(node);
                break;
            }

            if ((p->is_left() && node->is_left())
            || (p->is_right() && node->is_right())) {
                _zig_zig(node);
            } else {
                _zig_zag(node);
            }
        }
        set_root(node);
    }
    void _zig(Node* node) {
        // """Rotate node to root."""
        Node* p = node->get_parent();
        if (node->is_left()) {
            p->set_left(node->get_right());
            node->set_right(p);
        } else {
            p->set_right(node->get_left());
            node->set_left(p);
        }
        node->set_parent(nullptr);
    }
    void _zig_zig(Node* node) {
        // """Rotate left-left or right-right node."""
        Node* p = node->get_parent();
        Node* g = p->get_parent();

        if (node->is_left()) {
            rotate_right(g);
            rotate_right(p);
        } else {
            rotate_left(g);
            rotate_left(p);
        }
    }
    void _zig_zag(Node* node) {
        // """Rotate left-right node."""
        Node* p = node->get_parent();
        Node* g = p->get_parent();

        if (node->is_left()) {
            rotate_right(p);
            rotate_left(g);
        } else {
            rotate_left(p);
            rotate_right(g);
        }
    }
    Node* _find(Node* node) {
        // """Search node and splay."""
        Node* current = get_root();
        while (current && current->get_val() != node->get_val()) {
            if (current->get_val() < node->get_val()) {
                current = current->get_right();
            } else {
                current = current->get_left();
            }
        }
        _splay(current);
        return current;
    }
    Node* _find_by_pos(int pos) {
        // """Search node by pos and splay."""
        Node* node = get_root();
        if (!node || pos >= node->get_counter()) {
            throw "Position is out of range";
        }
        while (node) {
            if (node->get_right()) {
                if (pos < node->get_right()->get_counter()) {
                    node = node->get_right();
                    continue;
                }
                // # skip all right nodes
                pos -= node->get_right()->get_counter();
            }
            if (pos == 0) {
                break;
            }
            // # skip this node
            pos -= 1;
            node = node->get_left();
        }
        // # self._splay(node)
        return node;
    }
    void _merge(SplayTree* tree) {
        // """Merge trees."""
        if (!get_root()) {
            set_root(tree->get_root());
            return;
        }
        Node* node = most_right();
        _splay(node);
        node->set_right(tree->get_root());
    }
    myTuple _split(int val) {
        // """Split tree."""
        Node* node = get_root();
        Node* next_node = nullptr;

        SplayTree* left_tree = new SplayTree();
        SplayTree* right_tree = new SplayTree();

        if (!node) {
            // DONE: return tuple
            return std::make_tuple(left_tree, right_tree);
        }
        while (true) {
            if (node->get_val() > val) {
                next_node = node->get_left();
            } else {
                next_node = node->get_right();
            }
            if (!next_node) {
                break;
            }
            node = next_node;
        }
        _splay(node);
        if (node->get_val() <= val) {
            left_tree->set_root(node);
            right_tree->set_root(node->get_right());
            node->set_right(nullptr);
        } else {
            left_tree->set_root(node->get_left());
            right_tree->set_root(node);
            node->set_left(nullptr);
        }
        set_root(nullptr);
        // DONE: return tuple
        return std::make_tuple(left_tree, right_tree);
    }
    int _add(Node* node) {
        // """Add node."""
        // DONE: tuple
        SplayTree* tree1;
        SplayTree* tree2;
        std::tie(tree1, tree2) = _split(node->get_val());
        set_root(node);
        node->set_left(tree1->get_root());
        node->set_right(tree2->get_root());
        int pos = 0;
        if (node->get_right()) {
            pos = node->get_right()->get_counter();
        }
        delete tree1;
        delete tree2;
        return pos;
    }
    void _remove(Node* node) {
        // """Remove node."""
        _splay(node);
        set_root(node->get_left());
        SplayTree* right_tree = new SplayTree();
        right_tree->set_root(node->get_right());
        _merge(right_tree);
        delete right_tree;
    }
    // @property
    Node* most_left() {
        // """Most left leaf of tree."""
        int size = get_root()->get_counter();
        return _find_by_pos(size - 1);
    }
    // @property
    Node* most_right() {
        // """Most right leaf of tree."""
        return _find_by_pos(0);
    }
    void rotate_left(Node* node) {
        // """Rotate edge from node to right child counter -clockwise."""
        Node* child = node->get_right();

        int counter_node = node->get_counter();
        int counter_child = child->get_counter();

        Node* p = node->get_parent();
        if (p) {
            int counter_p = p->get_counter();
            if (node->is_left()) {
                p->set_left(child);
            } else {
                if (node->is_right()) {
                    p->set_right(child);
                }
            }
            p->set_counter(counter_p);
        }
        child->set_parent(p);

        // # child.left, node.right = node, child.left
        Node* grand_child = child->get_left();
        child->set_left(node);
        node->set_right(grand_child);

        node->set_counter(counter_node - counter_child);

        if (grand_child) {
            node->set_counter(node->get_counter() + grand_child->get_counter());
            counter_child -= grand_child->get_counter();
        }
        child->set_counter(counter_child + node->get_counter());
    }
    void rotate_right(Node* node) {
        // """Rotate edge from node to left child clockwise."""
        Node* child = node->get_left();

        int counter_node = node->get_counter();
        int counter_child = child->get_counter();

        Node* p = node->get_parent();
        if (p) {
            int counter_p = p->get_counter();
            if (node->is_left()) {
                p->set_left(child);
            } else {
                if (node->is_right()) {
                    p->set_right(child);
                }
            }
            p->set_counter(counter_p);
        }
        child->set_parent(p);

        // # child.right, node.left = node, child.right
        Node* grand_child = child->get_right();
        child->set_right(node);
        node->set_left(grand_child);

        node->set_counter(counter_node - counter_child);

        if (grand_child) {
            node->set_counter(node->get_counter() + grand_child->get_counter());
            counter_child -= grand_child->get_counter();
        }
        child->set_counter(counter_child + node->get_counter());
    }
};

class Worker {
    // """Worker."""
 public:
    SplayTree* tree;
    Worker() {
        // """Worker init."""
        tree = new SplayTree();
    }
    ~Worker() {
        // """Worker init."""
        delete tree;
    }
    // DONE: pairs for commands
    vector<int>* process(const vector<myCmd>& cmds, int size) {
        // """Process commands."""
        vector<int>* res = new vector<int>;
        for (auto it = cmds.begin(); it != cmds.end(); it++) {
            int cmd_code, x, pos;
            std::tie(cmd_code, x) = *it;
            switch (cmd_code) {
                case 1:
                    pos = tree->insert(x);
                    res->push_back(pos);
                    break;
                case 2:
                    tree->remove(x);
                    break;
                default:
                    throw "Invalid Command";
            }
        }
        return res;
    }
};


int main(void) {
    int n;

    std::cin >> n;
    vector<myCmd> cmds;

    for (int i = 0; i < n; i++) {
        int cmd, x;
        std::cin >> cmd >> x;
        myCmd t = std::make_tuple(cmd, x);
        cmds.push_back(t);
    }

    Worker* worker = new Worker();
    vector<int>* res = worker->process(cmds, cmds.size());

    for (auto it=res->begin(); it != res->end(); it++) {
        std::cout << *it << std::endl;
    }

    delete res;
    delete worker;
    return 0;
}
