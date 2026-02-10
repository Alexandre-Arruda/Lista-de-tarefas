# -*- coding: utf-8 -*-
"""Aplicativo de lista de tarefas com persistência em JSON.

Melhorias implementadas:
- armazenamento estruturado (id, texto, status e data de criação);
- interface interativa mais rica (concluir/reabrir/remover);
- validações de entrada;
- comandos rápidos via linha de comando (listar, adicionar, concluir, remover).
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
import argparse
import json
from pathlib import Path
from typing import Iterable

ARQUIVO_TAREFAS = Path("tarefas.json")


@dataclass
class Tarefa:
    id: int
    texto: str
    concluida: bool
    criada_em: str


def agora_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def carregar_tarefas(arquivo: Path = ARQUIVO_TAREFAS) -> list[Tarefa]:
    """Carrega tarefas de um arquivo JSON; retorna lista vazia se não existir."""
    if not arquivo.exists():
        return []

    try:
        dados = json.loads(arquivo.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

    tarefas: list[Tarefa] = []
    for item in dados:
        if not isinstance(item, dict):
            continue
        texto = str(item.get("texto", "")).strip()
        if not texto:
            continue
        tarefas.append(
            Tarefa(
                id=int(item.get("id", 0)) or int(datetime.now().timestamp() * 1000),
                texto=texto,
                concluida=bool(item.get("concluida", False)),
                criada_em=str(item.get("criada_em", agora_iso())),
            )
        )
    return tarefas


def salvar_tarefas(tarefas: Iterable[Tarefa], arquivo: Path = ARQUIVO_TAREFAS) -> None:
    """Salva as tarefas em JSON com indentação."""
    serializado = [asdict(tarefa) for tarefa in tarefas]
    arquivo.write_text(
        json.dumps(serializado, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def proximo_id(tarefas: list[Tarefa]) -> int:
    return (max((t.id for t in tarefas), default=0) + 1) if tarefas else 1


def listar_tarefas(tarefas: list[Tarefa]) -> None:
    print("\n--- Sua Lista de Tarefas ---")
    if not tarefas:
        print("Você não tem tarefas pendentes. Parabéns!")
    else:
        for i, tarefa in enumerate(tarefas, 1):
            marcador = "✓" if tarefa.concluida else " "
            print(f"{i}. [{marcador}] {tarefa.texto}")
    print("----------------------------\n")


def adicionar_tarefa(tarefas: list[Tarefa], texto: str) -> str:
    texto_limpo = texto.strip()
    if not texto_limpo:
        return "A tarefa não pode ser vazia."

    tarefa = Tarefa(
        id=proximo_id(tarefas),
        texto=texto_limpo,
        concluida=False,
        criada_em=agora_iso(),
    )
    tarefas.append(tarefa)
    return f"Tarefa '{texto_limpo}' adicionada com sucesso!"


def concluir_tarefa(tarefas: list[Tarefa], indice: int, concluida: bool = True) -> str:
    if indice < 1 or indice > len(tarefas):
        return "Número de tarefa inválido."

    tarefa = tarefas[indice - 1]
    tarefa.concluida = concluida
    return (
        f"Tarefa '{tarefa.texto}' marcada como concluída!"
        if concluida
        else f"Tarefa '{tarefa.texto}' reaberta."
    )


def remover_tarefa(tarefas: list[Tarefa], indice: int) -> str:
    if indice < 1 or indice > len(tarefas):
        return "Número de tarefa inválido."
    removida = tarefas.pop(indice - 1)
    return f"Tarefa '{removida.texto}' removida com sucesso!"


def mostrar_menu() -> None:
    print("O que você gostaria de fazer?")
    print("1. Listar tarefas")
    print("2. Adicionar nova tarefa")
    print("3. Concluir tarefa")
    print("4. Reabrir tarefa")
    print("5. Remover tarefa")
    print("6. Sair")


def solicitar_numero(mensagem: str) -> int | None:
    try:
        return int(input(mensagem).strip())
    except ValueError:
        print("Entrada inválida. Digite um número.")
        return None


def executar_modo_interativo() -> None:
    tarefas = carregar_tarefas()
    while True:
        mostrar_menu()
        escolha = input("Escolha uma opção (1-6): ").strip()

        if escolha == "1":
            listar_tarefas(tarefas)
        elif escolha == "2":
            texto = input("Digite a nova tarefa: ")
            print(adicionar_tarefa(tarefas, texto))
            salvar_tarefas(tarefas)
        elif escolha == "3":
            listar_tarefas(tarefas)
            numero = solicitar_numero("Número da tarefa para concluir: ")
            if numero is not None:
                print(concluir_tarefa(tarefas, numero, True))
                salvar_tarefas(tarefas)
        elif escolha == "4":
            listar_tarefas(tarefas)
            numero = solicitar_numero("Número da tarefa para reabrir: ")
            if numero is not None:
                print(concluir_tarefa(tarefas, numero, False))
                salvar_tarefas(tarefas)
        elif escolha == "5":
            listar_tarefas(tarefas)
            numero = solicitar_numero("Número da tarefa para remover: ")
            if numero is not None:
                print(remover_tarefa(tarefas, numero))
                salvar_tarefas(tarefas)
        elif escolha == "6":
            salvar_tarefas(tarefas)
            print("Até logo! Suas tarefas foram salvas.")
            break
        else:
            print("Opção inválida. Escolha um número entre 1 e 6.\n")


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gerenciador de tarefas")
    sub = parser.add_subparsers(dest="comando")

    sub.add_parser("listar", help="Lista tarefas")

    p_add = sub.add_parser("adicionar", help="Adiciona uma tarefa")
    p_add.add_argument("texto", help="Texto da tarefa")

    p_concluir = sub.add_parser("concluir", help="Conclui uma tarefa")
    p_concluir.add_argument("indice", type=int, help="Índice da tarefa")

    p_reabrir = sub.add_parser("reabrir", help="Reabre uma tarefa")
    p_reabrir.add_argument("indice", type=int, help="Índice da tarefa")

    p_remover = sub.add_parser("remover", help="Remove uma tarefa")
    p_remover.add_argument("indice", type=int, help="Índice da tarefa")

    return parser


def main() -> None:
    parser = construir_parser()
    args = parser.parse_args()

    if not args.comando:
        executar_modo_interativo()
        return

    tarefas = carregar_tarefas()

    if args.comando == "listar":
        listar_tarefas(tarefas)
        return

    if args.comando == "adicionar":
        print(adicionar_tarefa(tarefas, args.texto))
    elif args.comando == "concluir":
        print(concluir_tarefa(tarefas, args.indice, True))
    elif args.comando == "reabrir":
        print(concluir_tarefa(tarefas, args.indice, False))
    elif args.comando == "remover":
        print(remover_tarefa(tarefas, args.indice))

    salvar_tarefas(tarefas)


if __name__ == "__main__":
    main()
