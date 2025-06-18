import icontract 
from .no import BTreeNode 

# ==============================================================================
# CLASSE PARA A ÁRVORE-B
# ==============================================================================
@icontract.invariant(lambda self: self.root is None or self.root.n >= 1 or self.root.leaf, "A raiz deve ter pelo menos 1 chave, a menos que seja uma folha")
@icontract.invariant(lambda self: self.is_height_valid(), "Todos os nós folha devem estar no mesmo nível")
class BTree:
    """
    Implementação da Estrutura de Dados Árvore-B.

    Atributos:
        root (BTreeNode): A raiz da árvore.
        t (int): A ordem da árvore.
    """
    def __init__(self, t):
        """
        Inicializa a Árvore-B.

        Args:
            t (int): Ordem da árvore (mínimo de filhos). Deve ser >= 2.
        """
        if t < 2:
            raise ValueError("A ordem 't' da Árvore-B deve ser no mínimo 2.")
        self.root = BTreeNode(t, leaf=True)
        self.t = t

    def is_height_valid(self):
        """Verifica se todas as folhas estão no mesmo nível (Invariante)."""
        if self.root is None or not self.root.keys:
            return True
        level = self._get_leftmost_leaf_level(self.root)
        return self._check_all_leaves_level(self.root, level, 0)

    def _get_leftmost_leaf_level(self, node):
        level = 0
        curr = node
        while not curr.leaf:
            curr = curr.children[0]
            level += 1
        return level

    def _check_all_leaves_level(self, node, target_level, current_level):
        if node.leaf:
            return target_level == current_level
        for child in node.children:
            if not self._check_all_leaves_level(child, target_level, current_level + 1):
                return False
        return True

    # --------------------------------------------------------------------------
    # BUSCA
    # --------------------------------------------------------------------------
    def search(self, k):
        """
        Busca por uma chave 'k' na árvore.

        Retorna:
            O nó e o índice onde a chave foi encontrada, ou None.
        """
        return self._search_recursive(self.root, k)

    def _search_recursive(self, x, k):
        """Método auxiliar recursivo para a busca."""
        i = 0
        while i < x.n and k > x.keys[i]:
            i += 1
        if i < x.n and k == x.keys[i]:
            return (x, i)
        if x.leaf:
            return None
        return self._search_recursive(x.children[i], k)

    # --------------------------------------------------------------------------
    # INSERÇÃO
    # --------------------------------------------------------------------------
    @icontract.require(lambda self, k: self.search(k) is None, "A chave a ser inserida não deve existir na árvore")
    @icontract.ensure(lambda self, k, result: self.search(k) is not None, "A chave deve existir na árvore após a inserção")
    @icontract.ensure(
        lambda self: (1 <= self.root.n <= 2 * self.t - 1) or self.root.n == 0,
        "Pós-condição de chaves na raiz após inserção falhou."
    )
    def insert(self, k):
        """Insere uma nova chave 'k' na Árvore-B."""
        root = self.root
        # Se a raiz estiver cheia, a árvore cresce em altura
        if root.is_full():
            new_root = BTreeNode(self.t, leaf=False)
            self.root = new_root
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, k)
        else:
            self._insert_non_full(root, k)

    def _insert_non_full(self, x, k):
        """Insere uma chave 'k' em um nó 'x' que não está cheio."""
        i = x.n - 1
        if x.leaf:
            # Insere a chave na posição correta
            x.keys.append(0)
            while i >= 0 and k < x.keys[i]:
                x.keys[i+1] = x.keys[i]
                i -= 1
            x.keys[i+1] = k
            x.n += 1
        else:
            # Encontra o filho que deve receber a nova chave
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            # Se o filho estiver cheio, divide-o
            if x.children[i].is_full():
                self._split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self._insert_non_full(x.children[i], k)

    def _split_child(self, x, i):
        """Divide o i-ésimo filho de x, que está cheio."""
        t = self.t
        y = x.children[i]
        z = BTreeNode(t, y.leaf)
        z.n = t - 1

        # Move as últimas t-1 chaves de y para z
        for j in range(t - 1):
            z.keys.append(y.keys[j + t])
        
        # Se y não for folha, move os últimos t filhos de y para z
        if not y.leaf:
            for j in range(t):
                z.children.append(y.children[j + t])

        y.n = t - 1
        
        # Insere um novo filho em x
        x.children.insert(i + 1, z)
        # Move a chave mediana de y para x
        x.keys.insert(i, y.keys[t-1])
        x.n += 1
        
        # Limpa as chaves e filhos movidos de y
        y.keys = y.keys[0:t-1]
        if not y.leaf:
            y.children = y.children[0:t]

    # --------------------------------------------------------------------------
    # REMOÇÃO (Simplificada para demonstração)
    # --------------------------------------------------------------------------
    @icontract.require(lambda self, k: self.search(k) is not None, "A chave a ser removida deve existir na árvore")
    @icontract.ensure(lambda self, k, result: self.search(k) is None, "A chave não deve existir após a remoção")
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
                    succ_node = node.children[i+1]
                    if succ_node.n >= t:
                        succ = self._get_succ(succ_node)
                        node.keys[i] = succ
                        self._delete_recursive(succ_node, succ)
                    else:
                        self._merge(node, i)
                        self._delete_recursive(pred_node, k)
        elif not node.leaf:
            child_index_to_descend = i
            if i == node.n + 1:
                child_index_to_descend = i -1

            if node.children[child_index_to_descend].n < t:
                self._fill(node, child_index_to_descend)

            if i > node.n:
                self._delete_recursive(node.children[i-1], k)
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
        if i != 0 and node.children[i-1].n >= self.t:
            self._borrow_from_prev(node, i)
        elif i != node.n and node.children[i+1].n >= self.t:
            self._borrow_from_next(node, i)
        else:
            if i != node.n:
                self._merge(node, i)
            else:
                self._merge(node, i-1)

    def _borrow_from_prev(self, node, i):
        child = node.children[i]
        sibling = node.children[i-1]
        child.keys.insert(0, node.keys[i-1])
        node.keys[i-1] = sibling.keys.pop()
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        child.n += 1
        sibling.n -= 1

    def _borrow_from_next(self, node, i):
        child = node.children[i]
        sibling = node.children[i+1]
        child.keys.append(node.keys[i])
        node.keys[i] = sibling.keys.pop(0)
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        child.n += 1
        sibling.n -= 1
        
    def _merge(self, node, i):
        child = node.children[i]
        sibling = node.children[i+1]
        child.keys.append(node.keys.pop(i))
        child.keys.extend(sibling.keys)
        if not child.leaf:
            child.children.extend(sibling.children)
        child.n += sibling.n + 1
        node.children.pop(i+1)
        node.n -= 1

    # --------------------------------------------------------------------------
    # FUNÇÃO PARA IMPRESSÃO DA ÁRVORE
    # --------------------------------------------------------------------------
    def print_tree_pretty(self):
        """Imprime a árvore com uma estrutura de diretórios para melhor visualização."""
        print(f"Raiz: {self.root.keys}")
        self._print_recursive_pretty(self.root, "", True)
        
    def _print_recursive_pretty(self, node, prefix, is_last):
        """Método auxiliar recursivo para a impressão visual."""
        if not node.leaf:
            # Imprime os filhos antes para ter a estrutura correta
            for i, child in enumerate(node.children):
                is_current_last = (i == node.n)
                connector = "└── " if is_current_last else "├── "
                
                # O prefixo para os filhos é o prefixo atual mais a conexão
                child_prefix = prefix + ("    " if is_last else "│   ")
                
                # Imprime a conexão e as chaves do filho
                print(f"{child_prefix}{connector}{child.keys}")
                
                # Chamada recursiva para os filhos do filho
                self._print_recursive_pretty(child, child_prefix, is_current_last)
        
    def print_tree(self):
        """Imprime a árvore em um formato legível."""
        self._print_recursive(self.root, 0)

    def _print_recursive(self, x, level):
        """Método auxiliar recursivo para a impressão."""
        print(f"{'  ' * level}Nível {level}: {x.keys}")
        if not x.leaf:
            for i in range(x.n + 1):
                self._print_recursive(x.children[i], level + 1)