# from b_tree import BTree
from b_tree import BTree

def is_sorted(lst):
    return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))

def test_btree_imagem():
    print("Testando árvore baseada na imagem (t = 3)...")
    pontos = 0
    t = 3
    arvore = BTree(t)

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
        arvore.insert(v)

    if arvore.root:
        arvore.root.print_tree()


if __name__ == "__main__":
    test_btree_imagem()