import sys
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from matrix_.matrix import texto_efeito_pausa


class Testes(TestCase):
    @patch('matrix_.matrix.sleep')
    def test_texto_literal(self, _):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            texto_efeito_pausa('teste :)')
            imprimido = fake_out.getvalue()
        self.assertEqual('teste :)\n', imprimido)
