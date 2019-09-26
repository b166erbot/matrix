from functools import reduce
from os import get_terminal_size as get
from random import choice, shuffle, randint
from string import ascii_lowercase as string
from sys import stdout
from time import sleep
from itertools import dropwhile

from colored import attr, fg
# from cython import boundscheck, wraparound


def texto_efeito_pausa(texto: str):
    for a in texto:
        print(a, end='')
        stdout.flush()
        sleep(0.04)
    print()


class Character:
    cores = [fg('white'), fg('grey_89'), fg('grey_66'), fg('green'),
             fg('yellow'), fg('red')]

    def __init__(self, coluna):
        col, self.lin = get()
        self.cont = 0
        self.intervalo = coluna.intervalo
        self.coluna = coluna
        self.character = self.cores[3] + choice(string)

    def __add__(self, other):
        condicoes = [self.cont in self.intervalo, self.coluna.ativo]
        string = self.character if all(condicoes) else ' '
        self.cont += 1
        self.novo_char()
        return other.__radd__(string)

    def __radd__(self, other):
        condicoes = [self.cont in self.intervalo, self.coluna.ativo]
        string = self.character if all(condicoes) else ' '
        self.cont += 1
        self.novo_char()
        if isinstance(other, str):
            return other + string
        else:
            return other.character + string

    def __repr__(self):
        return self.character

    def __len__(self):
        return len(self.character)

    def novo_char(self):
        if self.cont in range(3):
            self.character = self.cores[int(self.cont)] + choice(string)
        else:
            self.character = self.cores[self.coluna.cor] + self.character[-1]


class UltimoCharacter(Character):
    def __add__(self, other):
        condicoes = [self.cont in self.intervalo, self.coluna.ativo]
        string = self.character if all(condicoes) else ' '
        if not self.cont < self.intervalo[-1] and self.coluna.ativo:
            self.coluna.ativo = False
        self.cont += 1
        self.novo_char()
        return other.__radd__(string)

    def __radd__(self, other):
        condicoes = [self.cont in self.intervalo, self.coluna.ativo]
        string = self.character if all(condicoes) else ' '
        if not self.cont < self.intervalo[-1] and self.coluna.ativo:
            self.coluna.ativo = False
        self.cont += 1
        self.novo_char()
        if isinstance(other, str):
            return other + string
        else:
            return other.character + string


class PulseCharacter(Character):
    def novo_char(self):
        if self.cont in range(3):
            self.character = self.cores[int(self.cont)] + choice(string)
        elif self.cont % 2 == 0:
            self.character = self.cores[0] + choice(string)


class RastroCharacter(Character):
    def __add__(self, other):
        condicoes = [self.cont > self.intervalo[0], self.coluna.ativo]
        string = self.character if all(condicoes) else ' '
        self.cont += 1
        self.novo_char()
        return other.__radd__(string)

    def __radd__(self, other):
        condicoes = [self.cont > self.intervalo[0], self.coluna.ativo]
        string = self.character if all(condicoes) else ' '
        self.cont += 1
        self.novo_char()
        if isinstance(other, str):
            return other + string
        else:
            return other.character + string

    def novo_char(self):
        if self.cont in range(3):
            self.character = self.cores[int(self.cont)] + choice(string)
        elif self.cont > self.intervalo[-1]:
            cha = self.coluna.arq.obter_cha(self.coluna)
            self.character = self.cores[0] + cha


# class InstavelCharacter(Character):
#     def __init__(self, *args):
#         super().__init__(*args)
#         self.velocidade = args[0].velocidade
#
#     def __add__(self, other):
#         condicoes = [self.cont in self.intervalo, self.coluna.ativo]
#         string = self.character if all(condicoes) else ' '
#         self.cont += self.velocidade
#         self.novo_char()
#         return other.__radd__(string)
#
#     def __radd__(self, other):
#         condicoes = [self.cont in self.intervalo, self.coluna.ativo]
#         string = self.character if all(condicoes) else ' '
#         self.cont += self.velocidade
#         self.novo_char()
#         if isinstance(other, str):
#             return other + string
#         else:
#            return other.character + string


class Coluna:
    def __init__(self, ativo=False, cor=3, rastro='', arq=''):
        colunas, linhas = get()
        self.intervalo = range(choice(range(4, linhas)))
        self.cha = [PulseCharacter(self) for x in range(3)]
        if rastro:
            self.rastro = rastro.center(colunas)
            self.cha += [Character(self) for x in range(linhas - 6)]
            shuffle(self.cha)
            self.cha.insert((linhas - 6) // 2, RastroCharacter(self))
        else:
            self.cha += [Character(self) for x in range(linhas - 5)]
            shuffle(self.cha)
        self.cha.append(UltimoCharacter(self))
        for numero, character in enumerate(self.cha):
            character.cont = -numero
        self.ativo = ativo
        self.cor = cor
        self.arq = arq

    def __iter__(self):
        return iter(self.cha)


# class ColunaInstavel(Coluna):
#     def __init__(self, ativo=False, cor=3, rastro='', arq=''):
#         self.velocidade = choice([0.5, 1.5])
#         colunas, linhas = get()
#         self.intervalo = range(choice(range(3, linhas)))
#         self.cha = [PulseCharacter(self) for x in range(3)]
#         if rastro:
#             self.rastro = rastro.center(colunas)
#             self.cha += [InstavelCharacter(self) for x in range(linhas - 6)]
#             shuffle(self.cha)
#             self.cha.insert((linhas - 6) // 2, RastroCharacter(self))
#         else:
#             self.cha += [InstavelCharacter(self) for x in range(linhas - 5)]
#             shuffle(self.cha)
#         self.cha.append(UltimoCharacter(self))
#         for numero, character in enumerate(self.cha):
#             character.cont = -numero
#         self.ativo = ativo
#         self.cor = cor
#         self.arq = arq


class Arquiteto:
    def __init__(self, rastro):
        self.c, l = get()
        self.colunas = [Coluna(rastro=rastro, arq=self) for a in range(self.c)]
        self._rastro = True if rastro else False
        if rastro:
            rastro = enumerate(rastro[:self.c].center(self.c))
            rastro = list(dropwhile(lambda x: x[1] == ' ', rastro))
            rastro = list(dropwhile(lambda x: x[1] == ' ', rastro[::-1]))
            rastro = list(map(lambda x: x[0], rastro[::-1]))
            self.marcar_rastro(rastro)

    def rain(self, stop=False):
        colunas, linhas = get()
        if not self._rastro:
            choice(self.colunas).ativo = True  # precisa iniciar a primeira
        while self.condicoes(colunas, linhas):  # por frames
            if not stop:
                self.sortear()
            gerador = zip(*self.colunas)
            gerador = (reduce(lambda x, y: x + y, z) for z in gerador)
            print(*gerador, sep='\n')
            sleep(0.04)  # velocidade dos frames

    def sortear(self):
        desativadas = [a for a in self.colunas if not a.ativo]
        if self.c - len(desativadas) < self.c//3:
            if not choice(range(20)) == 1:
                choice(desativadas).__init__(True,)
            else:
                choice(desativadas).__init__(True, choice((4, 5)))

    def marcar_rastro(self, rastro):
        for x in rastro:
            self.colunas[x].ativo = True
            for y in self.colunas[x].cha:
                y.intervalo = range(randint(4, 7))

    def condicoes(self, colunas, linhas) -> bool:
        tupla =  ([a for a in get()] == [colunas, linhas],
                  [x for x in self.colunas if x.ativo])
        return all(tupla)

    def obter_cha(self, coluna) -> str:
        return coluna.rastro[self.colunas.index(coluna)]


def main(rastro):
    texto_efeito_pausa('Conectando a matrix...')
    sleep(1)
    matrix = Arquiteto(rastro)
    try:
        matrix.rain()
    except KeyboardInterrupt:
        while matrix.condicoes(*get()):
            try:
                matrix.rain(True)
            except KeyboardInterrupt:
                pass
    print('\n' * get()[1])
    texto_efeito_pausa(attr(0) + '\nDesconectado.')


if __name__ == '__main__':
    main()

# TODO: deixar rastro na tela como palavras escrito algo, exemplo: matrix
# TODO: fazer com que as colunas se iniciem em lugares aleatórios na tela.
# TODO: fazer com que algumas fileiras fiquem mais rápidas e outras mais lentas
# TODO: tentar trazer os caracteres katakanas novamente? (god mode programming)

# todo 2
# todos os characters da coluna estão imprimindo, para que não ocorra, adicione
# um range de inicio e fim e verifique se o index do cha está nesse range no
# __(r)add__. não se esqueça de colocar o tamanho máximo (0, linhas) para o
# self.tamanho caso faça o segundo TODO.
