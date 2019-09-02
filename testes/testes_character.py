from string import ascii_lowercase as string
from unittest import TestCase
from unittest.mock import MagicMock, patch

from matrix_.matrixv2 import Character, UltimoCharacter


class TestesCharacter(TestCase):
    def setUp(self):
        mock, mock2 = MagicMock(), MagicMock()
        mock.ativo, mock.cor = True, 3
        mock2.ativo, mock2.cor = True, 3
        self.c = Character(-2, range(24), mock)
        self.d = Character(-2, range(24), mock2)

    def test_add_retornando_radd_com_erro_caso_other_igual_a_string(self):
        with self.assertRaises(AttributeError):
            self.c + ''

    def test_add_antes_do_intervalo_retornando_string_verde(self):
        temp = self.c + self.d
        self.assertRegex(self.c.character, r'\x1b\[38;5;2m\w')

    def test_add_depois_do_intervalo_retornando_string_verde(self):
        self.c.cont = 2
        temp = self.c + self.d
        self.assertRegex(self.c.character, r'\x1b\[38;5;2m\w')

    def test_add_cont_white(self):
        self.c.cont = -1
        temp = self.c + self.d
        self.assertRegex(self.c.character, r'\x1b\[38;5;15m\w')

    def test_add_cor_grey_89(self):
        self.c.cont = 0
        temp = self.c + self.d
        self.assertRegex(self.c.character, r'\x1b\[38;5;254m\w')

    def test_add_cor_grey_66(self):
        self.c.cont = 1
        temp = self.c + self.d
        self.assertRegex(self.c.character, r'\x1b\[38;5;248m\w')

    def test_add_variavel_cont_maior_que_limite_retornando_string_verde(self):
        self.c.cont = 29
        temp = self.c + self.d
        self.assertRegex(self.c.character, r'\x1b\[38;5;2m\w')

    def test_add_chamando_funcao_novo_char(self):
        mock = MagicMock()
        self.c.novo_char = mock
        temp = self.c + self.d
        mock.assert_any_call()

    def test_add_retorne_string_com_espaco_caso_condicoes_false(self):
        self.c.cont, self.c.intervalo = 0, range(-15, -13)
        mock = MagicMock()
        temp = self.c + mock
        mock.__radd__.assert_called_with(' ')

    def test_add_retorne_character_caso_condicoes_true(self):
        self.c.intervalo = range(-5, 5)
        mock = MagicMock()
        temp = self.c + mock
        argumento = mock.__radd__.call_args_list[0][0][0]
        self.assertRegex(argumento, r'\x1b\[38;5;2m\w')

    def test_radd_retornando_string_caso_other_seja_uma_string(self):
        self.assertEqual('' + self.c, ' ')

    def test_radd_antes_do_intervalo_retornando_string_verde(self):
        temp = ' ' + self.c
        self.assertRegex(self.c.character, r'\x1b\[38;5;2m\w')

    def test_radd_depois_do_intervalo_retornando_string_verde(self):
        self.c.cont = 2
        temp = ' ' + self.c
        self.assertRegex(self.c.character, r'\x1b\[38;5;2m\w')

    def test_radd_cont_white(self):
        self.c.cont = -1
        temp = ' ' + self.c
        self.assertRegex(self.c.character, r'\x1b\[38;5;15m\w')

    def test_radd_cor_grey_89(self):
        self.c.cont = 0
        temp = ' ' + self.c
        self.assertRegex(self.c.character, r'\x1b\[38;5;254m\w')

    def test_radd_cor_grey_66(self):
        self.c.cont = 1
        temp = ' ' + self.c
        self.assertRegex(self.c.character, r'\x1b\[38;5;248m\w')

    def test_radd_variavel_cont_maior_que_limite_retornando_string_verde(self):
        self.c.cont = 29
        temp = ' ' + self.c
        self.assertRegex(self.c.character, r'\x1b\[38;5;2m\w')

    def test_radd_chamando_funcao_novo_char(self):
        mock = MagicMock()
        self.c.novo_char = mock
        temp = ' ' + self.c
        mock.assert_any_call()

    def test_radd_retorne_string_com_espaco_caso_condicoes_false(self):
        self.c.cont, self.c.intervalo = 0, range(-15, -13)
        mock = MagicMock()
        temp = self.c.__radd__(mock)
        mock.character.__add__.assert_called_with(' ')

    def test_radd_retorne_character_caso_condicoes_true(self):
        self.c.intervalo = range(-5, 5)
        mock = MagicMock()
        temp = self.c.__radd__(mock)
        argumento = mock.character.__add__.call_args_list[0][0][0]
        self.assertRegex(argumento, r'\x1b\[38;5;2m\w')


class TestesUltimoCharacter(TestesCharacter):
    def setUp(self):
        mock, mock2 = MagicMock(), MagicMock()
        mock.ativo, mock.cor = True, 3
        mock2.ativo, mock2.cor = True, 3
        self.c = UltimoCharacter(-2, range(24), mock)
        self.d = Character(-2, range(24), mock2)

    def test_add_desativando_a_coluna_caso_var_cont_maior_que_intervalo(self):
        self.c.cont = 25
        temp = self.c + self.d
        self.assertFalse(self.c.coluna.ativo)

    def test_radd_desativando_a_coluna_caso_var_cont_maior_que_intervalo(self):
        self.c.cont = 25
        temp = self.c.__radd__(self.d)
        self.assertFalse(self.c.coluna.ativo)
