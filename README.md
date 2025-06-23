# Trabalho prático 1 (TPPE)

## 📝 Descrição

Este trabalho implementa uma **Árvore-B** em Python, utilizando o paradigma de **programação por contratos** com a biblioteca [icontract](https://icontract.readthedocs.io/en/latest/usage.html). A Árvore-B é uma estrutura de dados balanceada amplamente utilizada em sistemas de banco de dados e sistemas de arquivos para otimizar o acesso a grandes volumes de dados armazenados em memória secundária.

---

## 👥 Integrantes do Grupo

| Nome                                 | Matrícula |
| ------------------------------------ | --------- |
| Gabriel Marcolino Rodrigues          | 190087501 |
| Lucas Macedo Barboza                 | 190091720 |
| Luan Mateus Cesar Duarte             | 211041221 |
| Shaíne Aparecida Cardoso de Oliveira | 190134810 |
| Yago Milagres Passos                 | 200049879 |

---

## 📜 Programação por Contratos

A implementação utiliza **invariantes de classe**, **pré-condições** e **pós-condições** para garantir a correção das operações da Árvore-B, conforme exigido no enunciado do trabalho.

---

## 📁 Estrutura de Pastas e Arquivos

```
arvore_b/
├── __init__.py
├── b_tree.py
├── b_tree_node.py
├── main.py
│
├── test/
│   ├── test_b_tree.py
│   └── test_b_tree_node.py
│
README.md
requirements.txt
run_tests.sh
```

---

## 🚀 Como rodar

Você precisa ter [python 3](https://www.python.org/downloads/) instalado, e seu gerenciador de pacotes pip.

1. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Execute o programa principal:**

   ```bash
   python main.py
   ```

3. **Rode todos os testes:**
   ```bash
   ./run_tests.sh
   ```
   Ou, se preferir:
   ```bash
    python -m pytest arvore_b/test/
   ```

---

## Observações

- **Não** foi utilizado implementações prontas de Árvore-B de bibliotecas externas.
- A implementação seguiu o paradigma de orientação a objetos.
- Os contratos são implementados exclusivamente com a biblioteca [icontract](https://icontract.readthedocs.io/en/latest/usage.html).

---
