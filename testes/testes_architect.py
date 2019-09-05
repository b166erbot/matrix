from unittest import TestCase, skip
from unittest.mock import patch, MagicMock

from matrix_.matrix import Arquiteto, Coluna, get


class Testes(TestCase):
    def setUp(self):
        self.a = Arquiteto('')

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

    def test_sortear_ativando_colunas(self):
        self.a.sortear()
        condicao = any(a.ativo for a in self.a.colunas)
        self.assertTrue(condicao)

    def test_sortear_nao_sorteando_nenhuma_coluna_caso_colunas_ativas_sejam_maior_que_um_terco(self):
        self.a.c = 200
        self.a.sortear()
        condicao = any(a.ativo for a in self.a.colunas)
        self.assertFalse(condicao)

    @patch('matrix_.matrix.choice')
    def test_sortear_sorteando_uma_coluna_caso_range_de_25_diferente_de_1(self, mock):
        mock.side_effect = [2, self.a.colunas[3], 15, *list('b' * 80)]
        self.a.sortear()
        colunas = [1 for x in self.a.colunas if x.ativo]
        self.assertEqual(1, len(colunas))

    @patch('matrix_.matrix.choice')
    def test_sortear_sorteando_uma_coluna_ativa_caso_range_de_25_diferente_de_1(self, mock):
        mock.side_effect = [2, self.a.colunas[3], 15, *list('b' * 80)]
        self.a.sortear()
        coluna = next(filter(lambda x: x.ativo, self.a.colunas))
        self.assertTrue(coluna.ativo)

    @patch('matrix_.matrix.choice')
    def test_sortear_sorteando_uma_coluna_com_cor_3_caso_range_de_25_diferente_de_1(self, mock):
        mock.side_effect = [2, self.a.colunas[3], 15, *list('b' * 80)]
        self.a.sortear()
        coluna = next(filter(lambda x: x.ativo, self.a.colunas))
        cha = coluna.cha[-1]
        self.assertIn(cha.cores[3], cha.character)

    @patch('matrix_.matrix.choice')
    def test_sortear_sorteando_uma_coluna_caso_range_de_25_igual_a_1(self, mock):
        mock.side_effect = [1, self.a.colunas[3], 4, 15, *list('b' * 80)]
        self.a.sortear()
        colunas = [1 for x in self.a.colunas if x.ativo]
        self.assertEqual(1, len(colunas))

    @patch('matrix_.matrix.choice')
    def test_sortear_sorteando_uma_coluna_ativa_caso_range_de_25_igual_a_1(self, mock):
        mock.side_effect = [1, self.a.colunas[3], 4, 15, *list('b' * 80)]
        self.a.sortear()
        coluna = next(filter(lambda x: x.ativo, self.a.colunas))
        self.assertTrue(coluna.ativo)

    @patch('matrix_.matrix.choice')
    def test_sortear_sorteando_uma_coluna_com_cor_4_caso_range_de_25_igual_a_1(self, mock):
        mock.side_effect = [1, self.a.colunas[3], 4, 15, *list('b' * 80)]
        self.a.sortear()
        coluna = next(filter(lambda x: x.ativo, self.a.colunas))
        self.assertIs(coluna, self.a.colunas[3])
        self.assertEqual(coluna.cor, 4)

    @patch('matrix_.matrix.choice')
    def test_sortear_sorteando_uma_coluna_com_cor_5_caso_range_de_25_igual_a_1(self, mock):
        mock.side_effect = [1, self.a.colunas[3], 5, 15, *list('b' * 80)]
        self.a.sortear()
        coluna = next(filter(lambda x: x.ativo, self.a.colunas))
        self.assertIs(coluna, self.a.colunas[3])
        self.assertEqual(coluna.cor, 5)

    @patch('matrix_.matrix.sleep')
    @patch('matrix_.matrix.print')
    @patch('matrix_.matrix.choice')
    def test_rain_primeira_coluna_sendo_definida(self, choice, *_):
        mock = MagicMock(side_effect = (1, 0))
        self.a.condicoes = mock
        self.a.rain(False)
        self.assertIs(choice().ativo, True)

    @patch('matrix_.matrix.sleep')
    @patch('matrix_.matrix.print')
    @patch('matrix_.matrix.choice')
    def test_rain_stop_true_nao_chamando_sortear(self, *_):
        mock = MagicMock(side_effect = (1, 0))
        mock2 = MagicMock()
        self.a.condicoes = mock
        self.a.sortear = mock2
        self.a.rain(True)
        self.a.sortear.assert_not_called()

    @patch('matrix_.matrix.sleep')
    @patch('matrix_.matrix.print')
    @patch('matrix_.matrix.choice')
    def test_rain_stop_false_chamando_sortear(self, *_):
        mock = MagicMock(side_effect = (1, 0))
        mock2 = MagicMock()
        self.a.condicoes = mock
        self.a.sortear = mock2
        self.a.rain(False)
        self.a.sortear.assert_any_call()

    @patch('matrix_.matrix.sleep')
    @patch('matrix_.matrix.print')
    @patch('matrix_.matrix.choice')
    def test_rain_stop_sortear_sendo_chamando_25_vezes(self, *_):
        mock = MagicMock(side_effect = (1,) * 25 + (0,))
        mock2 = MagicMock()
        self.a.condicoes = mock
        self.a.sortear = mock2
        self.a.colunas = [MagicMock()]
        self.a.rain(False)
        vezes_chamado = self.a.sortear.call_count
        self.assertEqual(vezes_chamado, 25)

    def test_marcar_rastro_ativando_as_colunas(self):
        self.a.marcar_rastro(range(5, 10))
        todas_marcadas = all(self.a.colunas[x].ativo for x in range(5, 10))
        self.assertTrue(todas_marcadas)

    def test_marcar_rastro_ativando_somente_do_5_pra_frente(self):
        self.a.marcar_rastro(range(5, 10))
        todas_marcadas = all(self.a.colunas[x].ativo for x in range(4, 10))
        self.assertFalse(todas_marcadas)

    def test_marcar_rastro_ativando_somente_do_10_para_tras(self):
        self.a.marcar_rastro(range(5, 10))
        todas_marcadas = all(self.a.colunas[x].ativo for x in range(5, 11))
        self.assertFalse(todas_marcadas)

    def test_obter_cha_com_erro_caso_arquiteto_argumento_com_string_vazia(self):
        with self.assertRaises(AttributeError):
            self.a.obter_cha(self.a.colunas[0])

    def test_obter_cha_obter_caracter_m(self):
        self.a = Arquiteto('matrix')
        caracter = self.a.obter_cha(self.a.colunas[37])
        self.assertEqual(caracter, 'm')
