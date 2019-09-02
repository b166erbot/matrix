from unittest import TestCase

from matrix_.matrixv2 import Character, Coluna, UltimoCharacter


class TestColunaAtivoNaoAtivo(TestCase):
    def test_coluna_ativada(self):
        c = Coluna(True, 3)
        self.assertTrue(c.ativo)

    def test_ativo_caracteres_retornando_true_caso_coluna_ativada(self):
        c = Coluna(True, 3)
        self.assertTrue(all(x.ativo() for x in c))

    def test_coluna_desativada(self):
        c = Coluna(False, 3)
        self.assertFalse(c.ativo)

    def test_ativo_caracteres_retornando_false_caso_coluna_desativada(self):
        c = Coluna(False, 3)
        self.assertFalse(any(x.ativo() for x in c))


class DemaisTestes(TestCase):
    def setUp(self):
        self.c = Coluna(True, 3)

    def test_coluna_iteravel(self):
        gerador = (isinstance(a, (Character, UltimoCharacter)) for a in self.c)
        self.assertTrue(all(gerador))

    def test_verificar_se_todos_os_characteres_estao_no_devido_lugar(self):
        gerador = (isinstance(a, Character) for a in self.c.cha[:-1])
        self.assertTrue(all(gerador))

    def test_verificar_se_o_ultimo_character_esta_no_devido_lugar(self):
        self.assertIsInstance(self.c.cha[-1], UltimoCharacter)
