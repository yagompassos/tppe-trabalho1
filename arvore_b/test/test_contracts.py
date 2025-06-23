import pytest
from icontract.errors import ViolationError
from arvore_b.b_tree import BTree


def test_pre_condicao_insercao_viola():
    arvore = BTree(3)
    arvore.insert(10)
    with pytest.raises(ViolationError):
        arvore.insert(10)


def test_pre_condicao_remocao_viola():
    arvore = BTree(3)
    with pytest.raises(ViolationError):
        arvore.remove(10)


def test_pos_condicoes_após_insercao():
    arvore = BTree(3)
    arvore.insert(10)
    arvore.insert(20)
    arvore.insert(30)

    # As chaves devem estar dentro dos limites corretos
    for node in arvore._get_all_nodes():
        if node == arvore.root:
            assert 1 <= len(node.keys) <= 2 * arvore.t - 1
        else:
            assert arvore.t - 1 <= len(node.keys) <= 2 * arvore.t - 1


def test_pos_condicoes_após_remocao():
    arvore = BTree(3)
    for v in [10, 20, 30, 40, 50, 60]:
        arvore.insert(v)

    arvore.remove(20)
    arvore.remove(40)

    for node in arvore._get_all_nodes():
        if node == arvore.root:
            assert 1 <= len(node.keys) <= 2 * arvore.t - 1
        else:
            assert arvore.t - 1 <= len(node.keys) <= 2 * arvore.t - 1


def test_invariante_ordenacao_manual_violada():
    arvore = BTree(3)
    for v in [10, 20, 30]:
        arvore.insert(v)

    # Força violação da ordenação
    arvore.root.keys = [30, 10, 20]

    with pytest.raises(ViolationError):
        arvore.traverse()
