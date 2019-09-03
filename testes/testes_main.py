from unittest import TestCase, skip
from unittest.mock import call, patch

from matrix_.matrix import attr, main


class Testes(TestCase):
    @patch('matrix_.matrix.print')
    @patch('matrix_.matrix.sleep')
    @patch('matrix_.matrix.Architect')
    @patch('matrix_.matrix.texto_efeito_pausa')
    def test_texto_efeito_pausa_chamado_com_argumentos(self, mock2, *_):
        main()
        esperado = [
            call('Conectando a matrix...'), call(attr(0) + '\nDesconectado.')
        ]
        self.assertEqual(mock2.mock_calls, esperado)

    @patch('matrix_.matrix.print')
    @patch('matrix_.matrix.sleep')
    @patch('matrix_.matrix.texto_efeito_pausa')
    @patch('matrix_.matrix.Architect')
    def test_arquiteto_chamado(self, mock, *_):
        main()
        mock.assert_any_call()

    @skip
    @patch('matrix_.matrix.print')
    @patch('matrix_.matrix.sleep')
    @patch('matrix_.matrix.texto_efeito_pausa')
    @patch('matrix_.matrix.Architect.rain')
    def test_rain_chamado(self, mock, *_):
        main()
        mock.assert_any_call()
