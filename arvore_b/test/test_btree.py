import pytest
from arvore_b.b_tree import BTree


def is_sorted(lst):
    return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))


@pytest.fixture
def arvore():
    t = 3
    tree = BTree(t)
    valores = [
        40,
        20,
        60,
        10,
        30,
        50,
        70,
        90,
        15,
        12,
        18,
        25,
        35,
        45,
        5,
        7,
        55,
        65,
        75,
        80,
        85,
        92,
        95,
        98,
        99,
    ]
    for v in valores:
        tree.insert(v)
    return tree


def test_traversal_sorted(arvore):
    traversal = arvore.traverse()
    assert is_sorted(traversal)
    assert len(traversal) == 25


def test_busca_existente(arvore):
    assert arvore.search(25) is not None
    assert arvore.search(92) is not None


def test_busca_inexistente(arvore):
    assert arvore.search(1000) is None
    assert arvore.search(-10) is None


def test_remocao(arvore):
    arvore.remove(25)
    assert arvore.search(25) is None

    arvore.remove(30)
    assert arvore.search(30) is None

    arvore.remove(20)
    assert arvore.search(20) is None

    assert is_sorted(arvore.traverse())


def test_remocao_total():
    tree = BTree(3)
    valores = list(range(1, 21))
    for v in valores:
        tree.insert(v)

    for v in valores:
        assert tree.search(v) is not None
        tree.remove(v)
        assert tree.search(v) is None

    assert tree.traverse() == []
