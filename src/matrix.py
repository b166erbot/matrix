from functools import reduce
from itertools import dropwhile
from os import get_terminal_size as get
from random import choice, randint, shuffle
from string import ascii_lowercase as string
from time import sleep
from typing import Iterable, Union, NoReturn
from contextlib import suppress

from colored import attr, fg

# from cython import boundscheck, wraparound


def texto_efeito_pausa(texto: str) -> NoReturn:
    """ Função que imprime um texto como se alguém estivesse digitando. """
    for letra in texto:
        print(letra, end='', flush=True)
        sleep(0.04)
    print()


class Caracter:
    """ Classe que representa um caracter qualquer. """
    cores = [fg('white'), fg('grey_89'), fg('grey_66'), fg('green'),
             fg('yellow'), fg('red')]

    def __init__(self, coluna) -> NoReturn:
        col, self.lin = get()
        self.cont = 0
        self.intervalo = coluna.intervalo
        self.coluna = coluna
        self.character = self.cores[3] + choice(string)

    def __add__(self, other):
        condicoes = [self.cont in self.intervalo, self.coluna.ativo]
        string = self.character if all(condicoes) else ' '
        self.cont += 1
        self.character = self._novo_char()
        return other.__radd__(string)

    def __radd__(self, other):
        condicoes = [self.cont in self.intervalo, self.coluna.ativo]
        string = self.character if all(condicoes) else ' '
        self.cont += 1
        self.character = self._novo_char()
        if isinstance(other, str):
            char = other + string
        else:
            char = other.character + string
        return char

    def __repr__(self):
        return self.character

    def __len__(self) -> int:
        return len(self.character)

    def _novo_char(self) -> str:
        """ Método que gera um novo caracter. """
        if self.cont in range(3):
            char = self.cores[int(self.cont)] + choice(string)
        else:
            char = self.cores[self.coluna.cor] + self.character[-1]
        return char


class UltimoCaracter(Caracter):
    """ Classe que representa o ultimo caracter de uma coluna. """
    def __add__(self, other) -> Caracter:
        condicoes = [self.cont in self.intervalo, self.coluna.ativo]
        string = self.character if all(condicoes) else ' '
        if all((self.cont > self.intervalo[-1], self.coluna.ativo)):
            self.coluna.ativo = False
        self.cont += 1
        self.character = self._novo_char()
        return other.__radd__(string)

    def __radd__(self, other) -> Union[str, Caracter]:
        condicoes = [self.cont in self.intervalo, self.coluna.ativo]
        string = self.character if all(condicoes) else ' '
        if all((self.cont > self.intervalo[-1], self.coluna.ativo)):
            self.coluna.ativo = False
        self.cont += 1
        self.character = self._novo_char()
        if isinstance(other, str):
            char = other + string
        else:
            char = other.character + string
        return char


class PulseCaracter(Caracter):
    """
    Classe que representa o caracter que se auto modifica de tempos em tempos.
    """
    def _novo_char(self) -> str:
        """ Método que gera um novo caracter. """
        char = self.character
        if self.cont in range(3):
            char = self.cores[int(self.cont)] + choice(string)
        elif self.cont % 2 == 0:
            char = self.cores[0] + choice(string)
        return char


class RastroCaracter(Caracter):
    """
    Classe que representa o caracter que permanece quando a coluna termina.
    """
    def __add__(self, other) -> Caracter:
        condicoes = [self.cont > self.intervalo[0], self.coluna.ativo]
        string = self.character if all(condicoes) else ' '
        self.cont += 1
        self.character = self._novo_char()
        return other.__radd__(string)

    def __radd__(self, other) -> Union[str, Caracter]:
        condicoes = [self.cont > self.intervalo[0], self.coluna.ativo]
        string = self.character if all(condicoes) else ' '
        self.cont += 1
        self.character = self._novo_char()
        if isinstance(other, str):
            char = other + string
        else:
            char = other.character + string
        return char

    def _novo_char(self) -> str:
        """ Método que gera um novo caracter. """
        char = self.character
        if self.cont in range(3):
            char = self.cores[int(self.cont)] + choice(string)
        elif self.cont > self.intervalo[-1]:
            char = self.cores[0] + self.coluna.arq._obter_cha(self.coluna)
        return char


# class InstavelCaracter(Caracter):
#     def __init__(self, *args):
#         super().__init__(*args)
#         self.velocidade = args[0].velocidade
#
#     def __add__(self, other):
#         condicoes = [self.cont in self.intervalo, self.coluna.ativo]
#         string = self.character if all(condicoes) else ' '
#         self.cont += self.velocidade
#         self.character = self._novo_char()
#         return other.__radd__(string)
#
#     def __radd__(self, other):
#         condicoes = [self.cont in self.intervalo, self.coluna.ativo]
#         string = self.character if all(condicoes) else ' '
#         self.cont += self.velocidade
#         self.character = self._novo_char()
#         if isinstance(other, str):
#             char = other + string
#         else:
#             char = other.character + string
#         return char


class Coluna:
    """ Classe que alinha todos os caracteres em uma coluna. """
    def __init__(self, ativo=False, cor=3, rastro='', arq=''):
        colunas, linhas = get()
        self.intervalo = range(choice(range(4, linhas)))
        self.cha = list(map(PulseCaracter, (self,) * 3))
        if rastro:
            self.rastro = rastro.center(colunas)
            self.cha += list(map(Caracter, (self,) * (linhas - 6)))
            shuffle(self.cha)
            self.cha.insert((linhas - 6) // 2, RastroCaracter(self))
        else:
            self.cha += list(map(Caracter, (self,) * (linhas - 5)))
            shuffle(self.cha)
        self.cha.append(UltimoCaracter(self))
        for numero, character in enumerate(self.cha):
            character.cont = -numero
        self.ativo = ativo
        self.cor = cor
        self.arq = arq

    def __iter__(self) -> Iterable:
        """ Método que devolve todos os caracteres contidos na coluna. """
        return iter(self.cha)


# class ColunaInstavel(Coluna):
#     def __init__(self, ativo=False, cor=3, rastro='', arq=''):
#         self.velocidade = choice([0.5, 1.5])
#         colunas, linhas = get()
#         self.intervalo = range(choice(range(3, linhas)))
#         self.cha = [PulseCaracter(self) for x in range(3)]
#         if rastro:
#             self.rastro = rastro.center(colunas)
#             self.cha += [InstavelCaracter(self) for x in range(linhas - 6)]
#             shuffle(self.cha)
#             self.cha.insert((linhas - 6) // 2, RastroCaracter(self))
#         else:
#             self.cha += [InstavelCaracter(self) for x in range(linhas - 5)]
#             shuffle(self.cha)
#         self.cha.append(UltimoCaracter(self))
#         for numero, character in enumerate(self.cha):
#             character.cont = -numero
#         self.ativo = ativo
#         self.cor = cor
#         self.arq = arq


class Arquiteto:
    """ O arquiteto é o construtor da matrix. """
    def __init__(self, rastro: str) -> NoReturn:
        self.c, _ = get()
        self.colunas = [Coluna(rastro=rastro, arq=self) for a in range(self.c)]
        self._rastro = True if rastro else False
        if rastro:
            rastro = enumerate(rastro[:self.c].center(self.c))
            rastro = list(dropwhile(lambda x: x[1] == ' ', rastro))
            rastro = list(dropwhile(lambda x: x[1] == ' ', rastro[::-1]))
            rastro = list(map(lambda x: x[0], rastro[::-1]))
            self._marcar_rastro(rastro)

    def rain(self) -> NoReturn:
        with suppress(KeyboardInterrupt, EOFError):
            self._rodar()
        while self._condicoes(*get()):
            with suppress(KeyboardInterrupt, EOFError):
                self._rodar(True)

    def _rodar(self, stop=False) -> NoReturn:
        """ Método que imprime o efeito matrix na tela. """
        colunas, linhas = get()
        if not self._rastro:
            choice(self.colunas).ativo = True  # precisa iniciar a primeira
        while self._condicoes(colunas, linhas):  # por frames
            if not stop:
                self._sortear()
            gerador = zip(*self.colunas)
            gerador = (reduce(lambda x, y: x + y, z) for z in gerador)
            print(*gerador, sep='\n')
            sleep(0.04)  # velocidade dos frames

    def _sortear(self) -> NoReturn:
        """ Método que sorteia uma nova coluna para ser ativada. """
        desativadas = [a for a in self.colunas if not a.ativo]
        if self.c - len(desativadas) < self.c//3:
            if not choice(range(20)) == 1:
                choice(desativadas).__init__(True,)
            else:
                choice(desativadas).__init__(True, choice((4, 5)))

    def _marcar_rastro(self, rastro: list) -> NoReturn:
        """ Método que ativa todas as colunas que contém o rastro. """
        for x in rastro:
            self.colunas[x].ativo = True
            for y in self.colunas[x].cha:
                y.intervalo = range(randint(4, 7))

    def _condicoes(self, colunas: int, linhas: int) -> bool:
        """ Método que verifica se o loop no método rain deve continuar. """
        tupla = (list(get()) == [colunas, linhas],
                 [x for x in self.colunas if x.ativo])
        return all(tupla)

    def _obter_cha(self, coluna: Coluna) -> str:
        """
        Método que retorna o caracter rastro na posição do cha na coluna.
        """
        return coluna.rastro[self.colunas.index(coluna)]


def main(rastro: str) -> NoReturn:
    """ Função principal que roda o código. """
    texto_efeito_pausa('Conectando a matrix...')
    sleep(1)
    matrix = Arquiteto(rastro)
    matrix.rain()
    print('\n' * get()[1])
    texto_efeito_pausa(attr(0) + '\nDesconectado.')


# TODO: deixar rastro na tela como palavras escrito algo, exemplo: matrix
# TODO: fazer com que as colunas se iniciem em lugares aleatórios na tela.
# TODO: fazer com que algumas fileiras fiquem mais rápidas e outras mais lentas
# TODO: tentar trazer os caracteres katakanas novamente? (god mode programming)

# todo 2
# todos os characters da coluna estão imprimindo, para que não ocorra, adicione
# um range de inicio e fim e verifique se o index do cha está nesse range no
# __(r)add__. não se esqueça de colocar o tamanho máximo (0, linhas) para o
# self.tamanho caso faça o segundo TODO.
