from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.new_matrix import Coluna, Caracter


@patch('src.new_matrix.cor')
class TestColunaExibivel(TestCase):
    def setUp(self):
        self.tela = MagicMock()
        self.tela.getmaxyx.return_value = (80, 24)
        self.coluna = Coluna(self.tela, 24)

    @patch('src.new_matrix.curses')
    def test_exibir_exibindo_caso_coluna_ativa(self, *_):
        self.coluna.ativa = True
        for _ in range(5):
            self.coluna.exibir()
        self.tela.addstr.assert_called()

    def test_exibir_nao_exibindo_caso_coluna_nao_ativa(self, *_):
        self.coluna.exibir()
        self.tela.addstr.assert_not_called()


class TestColuna(TestCase):
    def setUp(self):
        self.tela = MagicMock()
        self.tela.getmaxyx.return_value = (80, 24)
        self.coluna = Coluna(self.tela, 24)
        self.caracter = Caracter(self.tela, MagicMock(return_value = True))

    # def test_exibivel_retornando_True_caso_caracter_estiver_na_distancia(self):
    #     self.coluna._distancia = range(50)
    #     resultado = self.coluna.exibivel(self.caracter)
    #     self.assertTrue(resultado)

    # def test_exibivel_retornando_False_caso_caracter_nao_estiver_na_distancia(
    #     self
    # ):
    #     self.coluna._distancia = range(-50, -1)
    #     resultado = self.coluna.exibivel(self.caracter)
    #     self.assertFalse(resultado)

    def test_desativar_coluna_desativando_a_coluna(self):
        self.coluna.ativa = True
        self.coluna.desativar_coluna()
        self.assertFalse(self.coluna.ativa)

    def test_reiniciar_coluna_reiniciando_a_coluna(self):
        self.coluna.__init__ = MagicMock()
        self.coluna._reiniciar_coluna()
        self.coluna.__init__.assert_called()

    # def test_andar_definindo_as_posicoes_caso_caminho_contenha_itens(self):
    #     mockado = MagicMock()
    #     caracter = self.coluna._caracteres[-1]
    #     caracter.definir_posicao = mockado
    #     self.coluna.andar()
    #     caracter.definir_posicao.assert_called()

    # def test_andar_nao_definindo_as_posicoes_caso_caminho_vazio(self):
    #     mockado = MagicMock()
    #     caracter = self.coluna._caracteres[-1]
    #     self.coluna._caminho = iter(range(0))  # iterável vazio
    #     caracter.definir_posicao = mockado
    #     self.coluna.andar()
    #     caracter.definir_posicao.assert_not_called()

    # def test_andar_definindo_a_posicao_do_primeiro_caracter(self):
    #     self.coluna.andar()
    #     self.assertNotEqual((0, 0), self.coluna._caracteres[0])

    # def test_andar_trocando_a_posicao_caso_seja_chamado_2_vezes(self):
    #     self.coluna.andar()
    #     self.coluna.andar()
    #     self.assertNotEqual((0, 0), self.coluna._caracteres[0].posicao)

    # def test_andar_trocando_a_posicao_do_segundo_caracter(self):
    #     self.coluna.andar()
    #     self.coluna.andar()
    #     self.assertNotEqual((0, 0), self.coluna._caracteres[1].posicao)
