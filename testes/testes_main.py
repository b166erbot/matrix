from unittest import TestCase, skip
from unittest.mock import call, patch

from matrix_.matrix import attr, main


class Testes(TestCase):
    @patch('matrix_.matrix.print')
    @patch('matrix_.matrix.sleep')
    @patch('matrix_.matrix.Arquiteto')
    @patch('matrix_.matrix.texto_efeito_pausa')
    def test_texto_efeito_pausa_chamado_com_argumentos(self, mock2, *_):
        main('')
        esperado = [
            call('Conectando a matrix...'), call(attr(0) + '\nDesconectado.')
        ]
        self.assertEqual(mock2.mock_calls, esperado)

    @patch('matrix_.matrix.print')
    @patch('matrix_.matrix.sleep')
    @patch('matrix_.matrix.texto_efeito_pausa')
    @patch('matrix_.matrix.Arquiteto')
    def test_arquiteto_chamado(self, mock, *_):
        main('')
        self.assertEqual(mock.call_count, 1)

    @patch('matrix_.matrix.print')
    @patch('matrix_.matrix.sleep')
    @patch('matrix_.matrix.texto_efeito_pausa')
    @patch('matrix_.matrix.Arquiteto.rain')
    def test_rain_chamado(self, mock, *_):
        main('')
        mock.assert_any_call()

    @patch('matrix_.matrix.print')
    @patch('matrix_.matrix.sleep')
    @patch('matrix_.matrix.texto_efeito_pausa')
    @patch('matrix_.matrix.Arquiteto.rain')
    def test_rain_nao_retornando_erro_de_KeyboardInterrupt(self, mock, *_):
        mock.side_effect = [KeyboardInterrupt(), 0]
        main('')
