# Lista de Tarefas

Projeto com duas interfaces:

- **Web (`index.html`)**: lista de tarefas moderna com filtros, pesquisa, edição rápida e import/export em JSON.
- **CLI (`lista_de_tarefas.py`)**: gerenciamento interativo ou via comandos no terminal.

## Recursos principais

### Web
- Tarefas por usuário (chave no `localStorage` com `userId`).
- Filtros: todas, ativas e concluídas.
- Pesquisa por texto.
- Barra de progresso de conclusão.
- Edição por duplo clique ou botão.
- Exportar/importar tarefas em JSON.

### CLI
- Persistência em `tarefas.json`.
- Suporte a tarefas concluídas e reabertas.
- Modo interativo e modo por comandos.

## Como usar (CLI)

### Modo interativo
```bash
python3 lista_de_tarefas.py
```

### Modo por comandos
```bash
python3 lista_de_tarefas.py listar
python3 lista_de_tarefas.py adicionar "Estudar Python"
python3 lista_de_tarefas.py concluir 1
python3 lista_de_tarefas.py reabrir 1
python3 lista_de_tarefas.py remover 1
```

## Testes

```bash
python3 -m unittest -v
```
