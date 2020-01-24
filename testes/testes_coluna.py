from unittest import TestCase

from src.matrix import Caracter, Coluna, UltimoCaracter


class Testes(TestCase):
    def setUp(self):
        self.c = Coluna(True, 3)

    def test_coluna_ativada(self):
        self.assertTrue(self.c.ativo)

    def test_ativo_caracteres_retornando_true_caso_coluna_ativada(self):
        self.assertTrue(all(x.coluna.ativo for x in self.c))

    def test_coluna_desativada(self):
        self.c = Coluna(False, 3)
        self.assertFalse(self.c.ativo)

    def test_ativo_caracteres_retornando_false_caso_coluna_desativada(self):
        self.c = Coluna(False, 3)
        self.assertFalse(any(x.coluna.ativo for x in self.c))

    def test_coluna_iteravel(self):
        gerador = (isinstance(a, (Caracter, UltimoCaracter)) for a in self.c)
        self.assertTrue(all(gerador))

    def test_verificar_se_todos_os_characteres_estao_no_devido_lugar(self):
        gerador = (isinstance(a, Caracter) for a in self.c.cha[:-1])
        self.assertTrue(all(gerador))

    def test_verificar_se_o_ultimo_character_esta_no_devido_lugar(self):
        self.assertIsInstance(self.c.cha[-1], UltimoCaracter)
