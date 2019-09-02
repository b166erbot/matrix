from unittest import TestCase, skip
from unittest.mock import patch

from matrix_.matrixv2 import Architect, Coluna, get


class Testes(TestCase):
    def setUp(self):
        self.a = Architect()

    def test_todas_as_colunas_sao_instancias_de_Coluna(self):
        instancias_colunas = (isinstance(x, Coluna) for x in self.a.colunas)
        self.assertTrue(all(instancias_colunas))

    def test_condicoes_retornando_true_caso_uma_coluna_ativa(self):
        self.a.colunas[0].ativo = True
        self.assertTrue(self.a.condicoes(*get()))

    def test_condicoes_retornando_false_caso_nao_haja_colunas_ativas(self):
        self.assertFalse(self.a.condicoes(*get()))

    def test_condicoes_retornando_false_caso_o_tamanho_da_tela_mude(self):
        self.a.colunas[0].ativo = True
        self.assertFalse(self.a.condicoes(1, 1))

    def test_condicoes_retornando_false_caso_sem_colunas_ativas_e_tela_desproporcional(self):
        self.assertFalse(self.a.condicoes(1, 1,))

    @skip
    def test_sortear_ativando_colunas(self):
        self.a.sortear()
        condicao = any(a.cha[-1].ativo() for a in self.a.colunas)
        self.assertTrue(condicao)

    @skip
    def test_sortear_nao_sorteando_nenhuma_coluna_caso_colunas_ativas_sejam_maior_que_um_terco(self):
        self.a.c = 200
        self.a.sortear()
        condicao = any(a.cha[-1].ativo() for a in self.a.colunas)
        self.assertFalse(condicao)

    @skip
    @patch('matrix_.matrixv2.choice')
    def test_sortear_sorteando_uma_coluna_caso_range_de_25_diferente_de_1(self, mock):
        mock.side_effect = [2, self.a.colunas[3], 15, *list('b' * 80)]
        self.a.sortear()
        colunas = [1 for x in self.a.colunas if x.cha[-1].ativo()]
        self.assertEqual(1, len(colunas))

    @skip
    @patch('matrix_.matrixv2.choice')
    def test_sortear_sorteando_uma_coluna_ativa_caso_range_de_25_diferente_de_1(self, mock):
        mock.side_effect = [2, self.a.colunas[3], 15, *list('b' * 80)]
        self.a.sortear()
        coluna = next(filter(lambda x: x.cha[-1].ativo(), self.a.colunas))
        self.assertTrue(coluna.ativo)

    @skip
    @patch('matrix_.matrixv2.choice')
    def test_sortear_sorteando_uma_coluna_com_cor_3_caso_range_de_25_diferente_de_1(self, mock):
        mock.side_effect = [2, self.a.colunas[3], 15, *list('b' * 80)]
        self.a.sortear()
        coluna = next(filter(lambda x: x.cha[-1].ativo(), self.a.colunas))
        cha = coluna.cha[-1]
        self.assertIn(cha.cores[3], cha.character)

    @skip
    @patch('matrix_.matrixv2.choice')
    def test_sortear_sorteando_uma_coluna_caso_range_de_25_igual_a_1(self, mock):
        mock.side_effect = [1, self.a.colunas[3], 4, 15, *list('b' * 80)]
        self.a.sortear()
        colunas = [1 for x in self.a.colunas if x.cha[-1].ativo()]
        self.assertEqual(1, len(colunas))

    @skip
    @patch('matrix_.matrixv2.choice')
    def test_sortear_sorteando_uma_coluna_ativa_caso_range_de_25_igual_a_1(self, mock):
        mock.side_effect = [1, self.a.colunas[3], 4, 15, *list('b' * 80)]
        self.a.sortear()
        coluna = next(filter(lambda x: x.cha[-1].ativo(), self.a.colunas))
        self.assertTrue(coluna.ativo)

    @skip
    @patch('matrix_.matrixv2.choice')
    def test_sortear_sorteando_uma_coluna_com_cor_4_caso_range_de_25_igual_a_1(self, mock):
        mock.side_effect = [1, self.a.colunas[3], 4, 15, *list('b' * 80)]
        self.a.sortear()
        coluna = next(filter(lambda x: x.cha[-1].ativo(), self.a.colunas))
        self.assertIs(coluna, self.a.colunas[3])
        self.assertEqual(coluna.cor, 4)

    @skip
    @patch('matrix_.matrixv2.choice')
    def test_sortear_sorteando_uma_coluna_com_cor_5_caso_range_de_25_igual_a_1(self, mock):
        mock.side_effect = [1, self.a.colunas[3], 5, 15, *list('b' * 80)]
        self.a.sortear()
        coluna = next(filter(lambda x: x.cha[-1].ativo(), self.a.colunas))
        self.assertIs(coluna, self.a.colunas[3])
        self.assertEqual(coluna.cor, 5)

# testes do rain não implementados
