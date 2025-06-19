import icontract
from .no import BTreeNode

# =====================================================================
# CLASSE PARA A ÁRVORE-B
# =====================================================================
@icontract.invariant(
    lambda self: self.root is None 
    or self.root.leaf 
    or (2 <= len(self.root.children) <= 2 * self.t),
    "A raiz (se não for folha) deve ter entre 2 e 2t filhos"
)
@icontract.invariant(
    lambda self: self.is_height_valid(),
    "Todos os nós folha devem estar no mesmo nível"
)
class BTree:
    """
    Implementação da Estrutura de Dados Árvore-B.
    """
    def __init__(self, t):
        if t < 2:
            raise ValueError("A ordem 't' da Árvore-B deve ser no mínimo 2.")
        self.t = t
        self.root = BTreeNode(t, leaf=True)

    # -----------------------------------------------------------------
    # INVARIANTE DE ALTURA (folhas no mesmo nível)
    # -----------------------------------------------------------------
    def is_height_valid(self):
        if self.root is None or not self.root.keys:
            return True
        level = self._get_leftmost_leaf_level(self.root)
        return self._check_all_leaves_level(self.root, level, 0)

    def _get_leftmost_leaf_level(self, node):
        level = 0
        current = node
        while not current.leaf:
            current = current.children[0]
            level += 1
        return level

    def _check_all_leaves_level(self, node, target_level, current_level):
        if node.leaf:
            return target_level == current_level
        for child in node.children:
            if not self._check_all_leaves_level(child, target_level, current_level + 1):
                return False
        return True

    # -----------------------------------------------------------------
    # BUSCA
    # -----------------------------------------------------------------
    def search(self, k):
        return self._search_recursive(self.root, k)

    def _search_recursive(self, node, k):
        i = 0
        while i < node.n and k > node.keys[i]:
            i += 1
        if i < node.n and node.keys[i] == k:
            return node, i
        if node.leaf:
            return None
        return self._search_recursive(node.children[i], k)

    # -----------------------------------------------------------------
    # INSERÇÃO
    # -----------------------------------------------------------------
    @icontract.require(
        lambda self, k: self.search(k) is None,
        "A chave a ser inserida não deve existir na árvore"
    )
    @icontract.ensure(
        lambda self, k, result: self.search(k) is not None,
        "A chave deve existir na árvore após a inserção"
    )
    @icontract.ensure(
        lambda self: (1 <= self.root.n <= 2 * self.t - 1) or self.root.n == 0,
        "Pós-condição: número de chaves na raiz após inserção"
    )
    def insert(self, k):
        root = self.root
        if root.is_full():
            new_root = BTreeNode(self.t, leaf=False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
            self._insert_non_full(new_root, k)
        else:
            self._insert_non_full(root, k)

    def _insert_non_full(self, node, k):
        i = node.n - 1
        if node.leaf:
            node.keys.append(0)
            while i >= 0 and k < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k
            node.n += 1
        else:
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            if node.children[i].is_full():
                self._split_child(node, i)
                if k > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], k)

    def _split_child(self, parent, index):
        t = self.t
        y = parent.children[index]
        z = BTreeNode(t, y.leaf)
        z.n = t - 1

        z.keys = y.keys[t: (2 * t - 1)]
        y.keys = y.keys[0: t - 1]

        if not y.leaf:
            z.children = y.children[t: (2 * t)]
            y.children = y.children[0: t]

        y.n = t - 1

        parent.children.insert(index + 1, z)
        parent.keys.insert(index, y.keys.pop())
        parent.n += 1

    # -----------------------------------------------------------------
    # REMOÇÃO
    # -----------------------------------------------------------------
    @icontract.require(
        lambda self, k: self.search(k) is not None,
        "A chave a ser removida deve existir na árvore"
    )
    @icontract.ensure(
        lambda self, k, result: self.search(k) is None,
        "A chave não deve existir na árvore após a remoção"
    )
    def delete(self, k):
        self._delete_recursive(self.root, k)
        if self.root.n == 0 and not self.root.leaf:
            self.root = self.root.children[0]

    def _delete_recursive(self, node, k):
        t = self.t
        i = 0
        while i < node.n and k > node.keys[i]:
            i += 1

        if i < node.n and node.keys[i] == k:
            if node.leaf:
                node.keys.pop(i)
                node.n -= 1
            else:
                pred_node = node.children[i]
                if pred_node.n >= t:
                    pred = self._get_pred(pred_node)
                    node.keys[i] = pred
                    self._delete_recursive(pred_node, pred)
                else:
                    succ_node = node.children[i + 1]
                    if succ_node.n >= t:
                        succ = self._get_succ(succ_node)
                        node.keys[i] = succ
                        self._delete_recursive(succ_node, succ)
                    else:
                        self._merge(node, i)
                        self._delete_recursive(pred_node, k)
        elif not node.leaf:
            if i == node.n:
                child_index = i - 1
            else:
                child_index = i

            if node.children[child_index].n < t:
                self._fill(node, child_index)

            if i > node.n:
                self._delete_recursive(node.children[i - 1], k)
            else:
                self._delete_recursive(node.children[i], k)

    def _get_pred(self, node):
        current = node
        while not current.leaf:
            current = current.children[current.n]
        return current.keys[-1]

    def _get_succ(self, node):
        current = node
        while not current.leaf:
            current = current.children[0]
        return current.keys[0]

    def _fill(self, node, i):
        if i != 0 and node.children[i - 1].n >= self.t:
            self._borrow_from_prev(node, i)
        elif i != node.n and node.children[i + 1].n >= self.t:
            self._borrow_from_next(node, i)
        else:
            if i != node.n:
                self._merge(node, i)
            else:
                self._merge(node, i - 1)

    def _borrow_from_prev(self, node, i):
        child = node.children[i]
        sibling = node.children[i - 1]
        child.keys.insert(0, node.keys[i - 1])
        node.keys[i - 1] = sibling.keys.pop()
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        child.n += 1
        sibling.n -= 1

    def _borrow_from_next(self, node, i):
        child = node.children[i]
        sibling = node.children[i + 1]
        child.keys.append(node.keys[i])
        node.keys[i] = sibling.keys.pop(0)
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        child.n += 1
        sibling.n -= 1

    def _merge(self, node, i):
        child = node.children[i]
        sibling = node.children[i + 1]
        child.keys.append(node.keys.pop(i))
        child.keys.extend(sibling.keys)
        if not child.leaf:
            child.children.extend(sibling.children)
        child.n += sibling.n + 1
        node.children.pop(i + 1)
        node.n -= 1

    # -----------------------------------------------------------------
    # IMPRESSÃO BONITA DA ÁRVORE
    # -----------------------------------------------------------------
    def print_tree_pretty(self):
        print(f"Raiz: {self.root.keys}")
        self._print_recursive_pretty(self.root, "", True)

    def _print_recursive_pretty(self, node, prefix, is_last):
        if not node.leaf:
            for i, child in enumerate(node.children):
                is_current_last = (i == node.n)
                connector = "└── " if is_current_last else "├── "
                child_prefix = prefix + ("    " if is_last else "│   ")
                print(f"{child_prefix}{connector}{child.keys}")
                self._print_recursive_pretty(child, child_prefix, is_current_last)
