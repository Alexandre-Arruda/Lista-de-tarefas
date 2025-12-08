# -*- coding: utf-8 -*-
import os

# Nome do arquivo onde as tarefas serão salvas
NOME_ARQUIVO = "tarefas.txt"

def carregar_tarefas():
    """Carrega as tarefas do arquivo de texto."""
    if not os.path.exists(NOME_ARQUIVO):
        return []
    with open(NOME_ARQUIVO, "r", encoding="utf-8") as f:
        tarefas = [linha.strip() for linha in f.readlines()]
    return tarefas

def salvar_tarefas(tarefas):
    """Salva a lista de tarefas no arquivo de texto."""
    with open(NOME_ARQUIVO, "w", encoding="utf-8") as f:
        for tarefa in tarefas:
            f.write(f"{tarefa}\n")

def listar_tarefas(tarefas):
    """Exibe a lista de tarefas numeradas."""
    print("\n--- Sua Lista de Tarefas ---")
    if not tarefas:
        print("Você não tem tarefas pendentes. Parabéns!")
    else:
        for i, tarefa in enumerate(tarefas, 1):
            print(f"{i}. {tarefa}")
    print("--------------------------\n")

def adicionar_tarefa(tarefas):
    """Adiciona uma nova tarefa à lista."""
    nova_tarefa = input("Digite a nova tarefa: ").strip()
    if nova_tarefa:
        tarefas.append(nova_tarefa)
        salvar_tarefas(tarefas)
        print(f"\nTarefa '{nova_tarefa}' adicionada com sucesso!")
    else:
        print("\nA tarefa não pode ser vazia.")

def remover_tarefa(tarefas):
    """Remove uma tarefa da lista pelo seu número."""
    listar_tarefas(tarefas)
    if not tarefas:
        return

    try:
        num_tarefa = int(input("Digite o número da tarefa que deseja remover: "))
        if 1 <= num_tarefa <= len(tarefas):
            tarefa_removida = tarefas.pop(num_tarefa - 1)
            salvar_tarefas(tarefas)
            print(f"\nTarefa '{tarefa_removida}' marcada como concluída!")
        else:
            print("\nNúmero de tarefa inválido.")
    except ValueError:
        print("\nEntrada inválida. Por favor, digite um número.")

def mostrar_menu():
    """Exibe o menu de opções."""
    print("\nO que você gostaria de fazer?")
    print("1. Listar tarefas")
    print("2. Adicionar uma nova tarefa")
    print("3. Remover uma tarefa (concluir)")
    print("4. Sair")

def main():
    """Função principal do programa."""
    tarefas = carregar_tarefas()
    while True:
        mostrar_menu()
        escolha = input("Escolha uma opção (1-4): ").strip()

        if escolha == "1":
            listar_tarefas(tarefas)
        elif escolha == "2":
            adicionar_tarefa(tarefas)
        elif escolha == "3":
            remover_tarefa(tarefas)
        elif escolha == "4":
            print("\nAté logo! Suas tarefas foram salvas.")
            break
        else:
            print("\nOpção inválida. Por favor, escolha um número entre 1 e 4.")

if __name__ == "__main__":
    main()
