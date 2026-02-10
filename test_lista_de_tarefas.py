import tempfile
import unittest
from pathlib import Path

from lista_de_tarefas import (
    Tarefa,
    adicionar_tarefa,
    carregar_tarefas,
    concluir_tarefa,
    remover_tarefa,
    salvar_tarefas,
)


class ListaDeTarefasTests(unittest.TestCase):
    def test_adicionar_tarefa_valida(self):
        tarefas = []
        msg = adicionar_tarefa(tarefas, "Nova tarefa")
        self.assertEqual(msg, "Tarefa 'Nova tarefa' adicionada com sucesso!")
        self.assertEqual(len(tarefas), 1)
        self.assertEqual(tarefas[0].texto, "Nova tarefa")

    def test_concluir_e_reabrir(self):
        tarefas = [Tarefa(id=1, texto="x", concluida=False, criada_em="2024-01-01T00:00:00")]
        self.assertIn("concluída", concluir_tarefa(tarefas, 1, True))
        self.assertTrue(tarefas[0].concluida)
        self.assertIn("reaberta", concluir_tarefa(tarefas, 1, False))
        self.assertFalse(tarefas[0].concluida)

    def test_remover_tarefa(self):
        tarefas = [Tarefa(id=1, texto="x", concluida=False, criada_em="2024-01-01T00:00:00")]
        msg = remover_tarefa(tarefas, 1)
        self.assertEqual(len(tarefas), 0)
        self.assertIn("removida", msg)

    def test_salvar_e_carregar_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            arquivo = Path(tmp) / "tarefas.json"
            original = [
                Tarefa(id=1, texto="A", concluida=False, criada_em="2024-01-01T00:00:00"),
                Tarefa(id=2, texto="B", concluida=True, criada_em="2024-01-02T00:00:00"),
            ]
            salvar_tarefas(original, arquivo)
            carregadas = carregar_tarefas(arquivo)
            self.assertEqual(len(carregadas), 2)
            self.assertEqual(carregadas[1].texto, "B")
            self.assertTrue(carregadas[1].concluida)


if __name__ == "__main__":
    unittest.main()
