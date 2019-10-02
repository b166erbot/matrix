from unittest import TestCase, skip
from unittest.mock import MagicMock

from matrix_.matrix import (Character, PulseCharacter, RastroCharacter,
                            UltimoCharacter)


class TestesCharacter(TestCase):
    def setUp(self):
        mock, mock2 = MagicMock(), MagicMock()
        mock.ativo, mock.cor, mock.intervalo = True, 3, range(24)
        mock2.ativo, mock2.cor, mock2.intervalo = True, 3, range(24)
        self.c = Character(mock)
        self.d = Character(mock2)
        self.c.cont = -2
        self.d.cont = -2

    def test_add_retornando_radd_com_erro_caso_other_igual_a_string(self):
        with self.assertRaises(AttributeError):
            self.c + ''

    def test_add_antes_do_intervalo_retornando_string_verde(self):
        self.c + self.d
        self.assertRegex(self.c.character, r'\x1b\[38;5;2m\w')

    def test_add_depois_do_intervalo_retornando_string_verde(self):
        self.c.cont = 2
        self.c + self.d
        self.assertRegex(self.c.character, r'\x1b\[38;5;2m\w')

    def test_add_cont_white(self):
        self.c.cont = -1
        self.c + self.d
        self.assertRegex(self.c.character, r'\x1b\[38;5;15m\w')

    def test_add_cor_grey_89(self):
        self.c.cont = 0
        self.c + self.d
        self.assertRegex(self.c.character, r'\x1b\[38;5;254m\w')

    def test_add_cor_grey_66(self):
        self.c.cont = 1
        self.c + self.d
        self.assertRegex(self.c.character, r'\x1b\[38;5;248m\w')

    def test_add_variavel_cont_maior_que_limite_retornando_string_verde(self):
        self.c.cont = 29
        self.c + self.d
        self.assertRegex(self.c.character, r'\x1b\[38;5;2m\w')

    def test_add_chamando_funcao_novo_char(self):
        mock = MagicMock()
        self.c.novo_char = mock
        self.c + self.d
        mock.assert_any_call()

    def test_add_retorne_string_com_espaco_caso_condicoes_false(self):
        self.c.cont, self.c.intervalo = 0, range(-15, -13)
        mock = MagicMock()
        self.c + mock
        mock.__radd__.assert_called_with(' ')

    def test_add_retorne_character_caso_condicoes_true(self):
        self.c.intervalo = range(-5, 5)
        mock = MagicMock()
        self.c + mock
        argumento = mock.__radd__.call_args_list[0][0][0]
        self.assertRegex(argumento, r'\x1b\[38;5;2m\w')

    def test_radd_retornando_string_caso_other_seja_uma_string(self):
        self.assertEqual('' + self.c, ' ')

    def test_radd_antes_do_intervalo_retornando_string_verde(self):
        self.c.__radd__(' ')
        self.assertRegex(self.c.character, r'\x1b\[38;5;2m\w')

    def test_radd_depois_do_intervalo_retornando_string_verde(self):
        self.c.cont = 2
        self.c.__radd__(' ')
        self.assertRegex(self.c.character, r'\x1b\[38;5;2m\w')

    def test_radd_cont_white(self):
        self.c.cont = -1
        self.c.__radd__(' ')
        self.assertRegex(self.c.character, r'\x1b\[38;5;15m\w')

    def test_radd_cor_grey_89(self):
        self.c.cont = 0
        self.c.__radd__(' ')
        self.assertRegex(self.c.character, r'\x1b\[38;5;254m\w')

    def test_radd_cor_grey_66(self):
        self.c.cont = 1
        self.c.__radd__(' ')
        self.assertRegex(self.c.character, r'\x1b\[38;5;248m\w')

    def test_radd_variavel_cont_maior_que_limite_retornando_string_verde(self):
        self.c.cont = 29
        self.c.__radd__(' ')
        self.assertRegex(self.c.character, r'\x1b\[38;5;2m\w')

    def test_radd_chamando_funcao_novo_char(self):
        mock = MagicMock()
        self.c.novo_char = mock
        self.c.__radd__(' ')
        mock.assert_any_call()

    def test_radd_retorne_string_com_espaco_caso_condicoes_false(self):
        self.c.cont, self.c.intervalo = 0, range(-15, -13)
        mock = MagicMock()
        self.c.__radd__(mock)
        mock.character.__add__.assert_called_with(' ')

    def test_radd_retorne_character_caso_condicoes_true(self):
        self.c.intervalo = range(-5, 5)
        mock = MagicMock()
        self.c.__radd__(mock)
        argumento = mock.character.__add__.call_args_list[0][0][0]
        self.assertRegex(argumento, r'\x1b\[38;5;2m\w')

    def test_repr_retornando_texto(self):
        temp = self.c + self.d
        self.assertEqual(repr(temp), "'  '")

    def test_len_retornando_o_tamanho_do_caracter(self):
        self.assertEqual(len(self.c), 10)

    def test_repr_retornando_o_caracter(self):
        self.assertRegex(repr(self.c), r'\x1b\[38;5;2m\w')

    def test_novo_char_retornando_caracter_branco_caso_cont_igual_a_0(self):
        self.c.cont = 0
        resultado = self.c.novo_char()
        self.assertRegex(resultado, r'\x1b\[38;5;15m\w')

    def test_novo_char_retornando_caracter_grey_89_caso_cont_igual_a_1(self):
        self.c.cont = 1
        resultado = self.c.novo_char()
        self.assertRegex(resultado, r'\x1b\[38;5;254m\w')

    def test_novo_char_retornando_caracter_grey_66_caso_cont_igual_a_2(self):
        self.c.cont = 2
        resultado = self.c.novo_char()
        self.assertRegex(resultado, r'\x1b\[38;5;248m\w')

    def test_novo_char_retornando_caracter_amarelo_caso_cont_fora_do_range_3(self):
        self.c.cont = 25
        self.c.character = 'o'
        self.c.coluna.cor = 4
        resultado = self.c.novo_char()
        self.assertRegex(resultado, r'\x1b\[38;5;3m\w')


class TestesUltimoCharacter(TestesCharacter):
    def setUp(self):
        mock, mock2 = MagicMock(), MagicMock()
        mock.ativo, mock.cor, mock.intervalo = True, 3, range(24)
        mock2.ativo, mock2.cor, mock2.intervalo = True, 3, range(24)
        self.c = UltimoCharacter(mock)
        self.d = Character(mock2)
        self.c.cont = -2
        self.d.cont = -2

    def test_add_desativando_a_coluna_caso_var_cont_maior_que_intervalo(self):
        self.c.cont = 25
        self.c + self.d
        self.assertFalse(self.c.coluna.ativo)

    def test_radd_desativando_a_coluna_caso_var_cont_maior_que_intervalo(self):
        self.c.cont = 25
        self.c.__radd__(self.d)
        self.assertFalse(self.c.coluna.ativo)


class TestesPulseCharacter(TestesCharacter):
    def setUp(self):
        mock, mock2 = MagicMock(), MagicMock()
        mock.ativo, mock.cor, mock.intervalo = True, 3, range(24)
        mock2.ativo, mock2.cor, mock2.intervalo = True, 3, range(24)
        mock.arq.obter_cha.return_value = 't'
        mock2.arq.obter_cha.return_value = 't'
        self.c = PulseCharacter(mock)
        self.d = PulseCharacter(mock2)
        self.c.cont = -2
        self.d.cont = -2

    @skip
    def test_radd_variavel_cont_maior_que_limite_retornando_string_verde(self):
        pass

    def test_radd_variavel_cont_maior_que_limite_retornando_string_branca(self):
        self.c.cont = 29
        self.c.__radd__(' ')
        self.assertRegex(self.c.character, r'\x1b\[38;5;15m\w')

    @skip
    def test_add_variavel_cont_maior_que_limite_retornando_string_verde(self):
        pass

    def test_add_variavel_cont_maior_que_limite_retornando_string_branca(self):
        self.c.cont = 29
        self.c + self.d
        self.assertRegex(self.c.character, r'\x1b\[38;5;15m\w')

    def test_novo_char_retornando_caracter_white_caso_cont_seja_positivo(self):
        self.c.cont = 4
        resultado = self.c.novo_char()
        self.assertRegex(resultado, r'\x1b\[38;5;15m\w')

    @skip
    def test_novo_char_retornando_caracter_amarelo_caso_cont_fora_do_range_3(self):
        pass


class TestesRastroCharacter(TestesCharacter):
    def setUp(self):
        mock, mock2 = MagicMock(), MagicMock()
        mock.ativo, mock.cor, mock.intervalo = True, 3, range(24)
        mock2.ativo, mock2.cor, mock2.intervalo = True, 3, range(24)
        self.c = RastroCharacter(mock)
        self.d = RastroCharacter(mock2)
        self.c.cont = -2
        self.d.cont = -2

    def test_radd_retorne_string_com_espaco_caso_condicoes_false(self):
        self.c.cont, self.c.intervalo = -16, range(-15, -13)
        mock = MagicMock()
        self.c.__radd__(mock)
        mock.character.__add__.assert_called_with(' ')

    def test_add_retorne_string_com_espaco_caso_condicoes_false(self):
        self.c.cont, self.c.intervalo = -16, range(-15, -13)
        mock = MagicMock()
        self.c + mock
        mock.__radd__.assert_called_with(' ')

    def test_radd_variavel_cont_maior_que_limite_retornando_string_verde(self):
        self.c.count = 200
        self.c + self.d
        self.assertRegex(self.c.character, r'\x1b\[38;5;2m\w')

    def test_novo_char_retornando_caracter_white_caso_cont_maior_intervalo(self):
        self.c.cont = 25
        self.c.coluna.arq.obter_cha.return_value = 'o'
        resultado = self.c.novo_char()
        self.assertRegex(resultado, r'\x1b\[38;5;15m\w')

    @skip('não sei como testar ainda')
    def test_radd_variavel_cont_maior_que_limite_retornando_string_branca(self):
        # self.c.character = ???
        # self.c.cont = 29
        # self.c.__radd__(' ')
        # self.assertRegex(self.c.character, r'\x1b\[38;5;15m\w')
        pass

    @skip
    def test_add_variavel_cont_maior_que_limite_retornando_string_verde(self):
        pass

    @skip
    def test_novo_char_retornando_caracter_amarelo_caso_cont_fora_do_range_3(self):
        pass
