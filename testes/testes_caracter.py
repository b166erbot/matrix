from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.new_matrix import Caracter, UltimoCaracter


class TestCaracter(TestCase):
    pass


# @patch('src.new_matrix.cor')
# class TestCaracterExibivel(TestCase):
#     def setUp(self):
#         self.tela = MagicMock()
#         self.exibivel = MagicMock(return_value = True)
#         self.caracter = Caracter(self.tela, self.exibivel)
#         self.caracter.posicao = (0, 1)
#
#     def test_exibindo_caracter_na_tela_caso_posicao_0_1(self, *_):
#         self.caracter.exibir()
#         self.tela.addstr.assert_called()
#
#     def test_exibir_nao_exibindo_caracter_na_tela_caso_posicao_0_0(
#         self, *_
#     ):
#         self.caracter.posicao = (0, 0)
#         self.caracter.exibir()
#         self.tela.addstr.assert_not_called()
#
#     def test_exibir_nao_limpando_o_caracter_caso_exibivel_True(self, *_):
#         self.caracter.exibir()
#         self.assertNotEqual(self.caracter._caracter, ' ')


# class TestCaracterDefinir_posicao(TestCase):
#     def setUp(self):
#         self.tela = MagicMock()
#         self.exibivel = MagicMock(return_value = True)
#         self.caracter = Caracter(self.tela, self.exibivel)
#         self.caracter.posicao = (0, 1)
#         self.caracter.posicao_anterior = (0, 1)
#
#     def test_definindo_uma_nova_posicao_caso_caracter_seja_tupla(self):
#         self.caracter.definir_posicao((1, 1))
#         self.assertEqual((1, 1), self.caracter.posicao)
#
#     def test_definindo_uma_nova_posicao_caso_caracter_seja_instancia_Caracter(
#         self
#     ):
#         caracter = Caracter(MagicMock(), MagicMock())
#         caracter.posicao_anterior = caracter.posicao = (2, 2)
#         self.caracter.definir_posicao(caracter)
#         self.assertEqual((2, 2), self.caracter.posicao)


# @patch('src.new_matrix.cor')
# class TestUltimoCaracterExibivel(TestCaracterExibivel):
#     def setUp(self):
#         # super().setUp()  primeiro teste não funcionou
#         self.tela = MagicMock()
#         self.exibivel = MagicMock(return_value = True)
#         self.caracter = UltimoCaracter(
#             self.tela, self.exibivel, desativar_coluna = MagicMock()
#         )
#         self.caracter.posicao = (0, 1)


# class TestUltimoCaracterDefinir_posicao(TestCaracterDefinir_posicao):
#     def setUp(self):
#         super().setUp()
#         self.caracter = UltimoCaracter(
#             self.tela, self.exibivel, desativar_coluna = MagicMock()
#         )
#
#     def test_definir_posicao_ativando_a_coluna_caso_exibivel_retorne_True(self):
#         self.assertFalse(self.caracter._ativo)
#         self.caracter.definir_posicao((0, 1))
#         self.assertTrue(self.caracter._ativo)
#
#     def test_definir_posicao_nao_ativando_a_coluna_caso_exibivel_retorne_False(
#         self
#     ):
#         self.assertFalse(self.caracter._ativo)
#         self.exibivel.return_value = False
#         self.caracter.definir_posicao((0, 1))
#         self.assertFalse(self.caracter._ativo)
