from arvore_b.arvore import BTree
# ==============================================================================
# BLOCO DE EXECUÇÃO PRINCIPAL
# ==============================================================================
def main():
    print("Iniciando a demonstração da Árvore-B com ordem t=3.")

    # Criação da Árvore-B com ordem 3, conforme o exemplo do documento
    b_tree = BTree(t=3)

    # Inserindo os valores do exemplo
    valores_exemplo = [10, 20, 40, 30, 50, 60, 70, 80, 90, 95, 15, 5, 7, 12, 18, 25, 35, 45, 55, 65, 75, 85, 92, 98, 99]
    print(f"\nInserindo os seguintes valores na árvore: {sorted(valores_exemplo)}")

    for val in sorted(valores_exemplo): # Inserir em ordem facilita a visualização
        print(f"--- Inserindo {val} ---")
        b_tree.insert(val)
    
    print("\n--- Estrutura Final da Árvore-B ---")
    b_tree.print_tree_pretty()

    print("\n--- Testando a Busca ---")
    chaves_para_buscar = [40, 75, 99, 100]
    for chave in chaves_para_buscar:
        resultado = b_tree.search(chave)
        if resultado:
            print(f"Chave {chave} encontrada.")
        else:
            print(f"Chave {chave} NÃO encontrada.")
            
    print("\n--- Testando a Remoção ---")
    chaves_para_remover = [20, 60, 7] # Testando remoção de nó interno, folha, etc.
    
    for chave in chaves_para_remover:
        print(f"\nRemovendo a chave {chave}...")
        try:
            b_tree.delete(chave)
            print(f"Chave {chave} removida com sucesso.")
            print("Estrutura da árvore agora:")
            b_tree.print_tree_pretty()
        except Exception as e:
            print(f"Erro ao remover a chave {chave}: {e}")
            
    print("\nVerificando se as chaves foram removidas...")
    for chave in chaves_para_remover:
        if b_tree.search(chave) is None:
            print(f"Confirmação: Chave {chave} NÃO está mais na árvore.")
        else:
            print(f"ERRO: Chave {chave} AINDA está na árvore.")

    print("\nDemonstração finalizada.")
    
# O if __name__ == "__main__" garante que a função main() só será executada
# quando você rodar este arquivo diretamente.
if __name__ == "__main__":
    main()