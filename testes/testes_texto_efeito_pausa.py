from unittest import TestCase
from unittest.mock import patch
import sys
from io import StringIO
from matrix_.matrixv2 import texto_efeito_pausa


class Testes(TestCase):
    @patch('matrix_.matrixv2.sleep')
    def test_texto_literal(self, _):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            texto_efeito_pausa('teste :)')
            imprimido = fake_out.getvalue()
        self.assertEqual('teste :)\n', imprimido)
