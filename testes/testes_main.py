from unittest import TestCase, skip
from unittest.mock import MagicMock, call, patch

from src.matrix import attr, main


class Testes(TestCase):
    @patch('src.matrix.print')
    @patch('src.matrix.sleep')
    @patch('src.matrix.Arquiteto')
    @patch('src.matrix.texto_efeito_pausa')
    def test_texto_efeito_pausa_chamado_com_argumentos(self, mock2, *_):
        main('')
        esperado = [
            call('Conectando a matrix...'), call(attr(0) + '\nDesconectado.')
        ]
        self.assertEqual(mock2.mock_calls, esperado)

    @patch('src.matrix.print')
    @patch('src.matrix.sleep')
    @patch('src.matrix.texto_efeito_pausa')
    @patch('src.matrix.Arquiteto')
    def test_arquiteto_chamado(self, mock, *_):
        main('')
        self.assertEqual(mock.call_count, 1)

    @patch('src.matrix.print')
    @patch('src.matrix.sleep')
    @patch('src.matrix.texto_efeito_pausa')
    @patch('src.matrix.Arquiteto.rain')
    def test_rain_chamado(self, mock, *_):
        main('')
        mock.assert_any_call()

    @patch('src.matrix.print')
    @patch('src.matrix.sleep')
    @patch('src.matrix.texto_efeito_pausa')
    @patch('src.matrix.Arquiteto._rodar')
    def test_rodar_nao_retornando_erro_de_KeyboardInterrupt(self, mock, *_):
        mock.side_effect = [KeyboardInterrupt()]
        main('')
        self.assertEqual(mock.call_count, 1)

    @patch('src.matrix.print')
    @patch('src.matrix.sleep')
    @patch('src.matrix.texto_efeito_pausa')
    @patch('src.matrix.Arquiteto._rodar')
    @patch('src.matrix.Arquiteto._condicoes', side_effect=[True] * 3 + [False])
    def test_rodar_nao_retornando_erro_de_KeyboardInterrupt_2(
        self, condicoes, rodar, *_
    ):
        rodar.side_effect = [KeyboardInterrupt()] * 3 + [0]
        main('')
        self.assertEqual(condicoes.call_count, 4)
