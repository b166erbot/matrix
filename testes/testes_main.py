from unittest import TestCase, skip
from unittest.mock import call, patch

from matrix_.matrixv2 import attr, main


class Testes(TestCase):
    @patch('matrix_.matrixv2.print')
    @patch('matrix_.matrixv2.sleep')
    @patch('matrix_.matrixv2.Architect')
    @patch('matrix_.matrixv2.texto_efeito_pausa')
    def test_texto_efeito_pausa_chamado_com_argumentos(self, mock2, *_):
        main()
        esperado = [
            call('Conectando a matrix...'), call(attr(0) + '\nDesconectado.')
        ]
        self.assertEqual(mock2.mock_calls, esperado)

    @patch('matrix_.matrixv2.print')
    @patch('matrix_.matrixv2.sleep')
    @patch('matrix_.matrixv2.texto_efeito_pausa')
    @patch('matrix_.matrixv2.Architect')
    def test_arquiteto_chamado(self, mock, *_):
        main()
        mock.assert_any_call()

    @skip
    @patch('matrix_.matrixv2.print')
    @patch('matrix_.matrixv2.sleep')
    @patch('matrix_.matrixv2.texto_efeito_pausa')
    @patch('matrix_.matrixv2.Architect.rain')
    def test_rain_chamado(self, mock, *_):
        main()
        mock.assert_any_call()

    @patch('matrix_.matrixv2.print')
    @patch('matrix_.matrixv2.sleep')
    @patch('matrix_.matrixv2.texto_efeito_pausa')
    @patch('matrix_.matrixv2.Architect.rain')
    @patch('matrix_.matrixv2.Architect.tarefas_assincronas')
    def test_chamando_metodo_tarefas_assincronas(self, mock, *_):
        main()
        mock.assert_any_call()
