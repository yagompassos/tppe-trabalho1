import icontract

# =====================================================================
# CLASSE PARA O NÓ DA ÁRVORE-B
# =====================================================================
@icontract.invariant(
    lambda self: self.leaf or (self.n + 1 == len(self.children)),
    "Se não é folha, o número de filhos deve ser igual ao número de chaves + 1"
)
@icontract.invariant(
    lambda self: self.n <= (2 * self.t) - 1,
    "Nenhum nó pode ter mais do que 2t - 1 chaves"
)
@icontract.invariant(
    lambda self: self.leaf or (self.t <= len(self.children) <= 2 * self.t),
    "Se não é folha, o número de filhos deve estar entre t e 2t"
)
@icontract.invariant(
    lambda self: all(self.keys[i] < self.keys[i + 1] for i in range(len(self.keys) - 1)),
    "As chaves no nó devem estar em ordem crescente"
)
class BTreeNode:
    """
    Um nó da Árvore-B.

    Atributos:
        t (int): Ordem da árvore.
        keys (list): Lista de chaves.
        children (list): Lista de filhos.
        leaf (bool): Se é uma folha.
        n (int): Número atual de chaves.
    """
    def __init__(self, t, leaf=False):
        self.t = t
        self.keys = []
        self.children = []
        self.leaf = leaf
        self.n = 0

    def is_full(self):
        """Verifica se o nó está cheio."""
        return self.n == (2 * self.t) - 1
