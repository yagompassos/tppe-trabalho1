import icontract

# ==============================================================================
# CLASSE PARA O NÓ DA ÁRVORE-B
# ==============================================================================
# A CORREÇÃO ESTÁ NA LINHA DA INVARIANTE A SEGUIR
@icontract.invariant(lambda self: self.leaf or self.n == 0 or len(self.children) == self.n + 1, "Um nó interno com chaves deve ter n+1 filhos")
@icontract.invariant(lambda self: self.n <= (2 * self.t) - 1, "Um nó não pode ter mais que 2t-1 chaves")
@icontract.invariant(lambda self: all(self.keys[i] < self.keys[i+1] for i in range(self.n - 1)), "As chaves de um nó devem estar em ordem crescente")
class BTreeNode:
    """
    Um nó da Árvore-B.

    Atributos:
        t (int): A ordem da árvore.
        keys (list): Lista de chaves no nó.
        children (list): Lista de filhos do nó.
        leaf (bool): True se o nó é uma folha, False caso contrário.
        n (int): Número atual de chaves no nó.
    """
    def __init__(self, t, leaf=False):
        """Inicializa um nó da Árvore-B."""
        self.t = t
        self.keys = []
        self.children = []
        self.leaf = leaf
        self.n = 0

    def is_full(self):
        """Verifica se o nó está cheio."""
        return self.n == (2 * self.t) - 1
