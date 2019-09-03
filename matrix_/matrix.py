from functools import reduce
from os import get_terminal_size as get
from random import choice, shuffle, randint
from string import ascii_lowercase as string
from sys import stdout
from time import sleep

from colored import attr, fg
# from cython import boundscheck, wraparound


def texto_efeito_pausa(texto: str):
    for a in texto:
        print(a, end='')
        stdout.flush()
        sleep(0.04)
    print()


class Character:
    cores = {0: fg('white'),
             1: fg('grey_89'),
             2: fg('grey_66'),
             3: fg('green'),
             4: fg('yellow'),
             5: fg('red')}

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

    def __iter__(self):
        return self

    def ativo(self):
        if self.coluna and self.coluna.ativo:
            return True
        return False

    def novo_char(self):
        if self.cont in range(3):
            self.character = self.cores[self.cont] + choice(string)
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
            self.character = self.cores[self.cont] + choice(string)
        elif self.cont % 2 == 0:
            self.character = self.cores[0] + choice(string)


class Coluna:
    # talvez a resposta para o inicio da coluna esteja na função range do
    # Character.novo_char
    def __init__(self, ativo=False, cor=3):
        colunas, linhas = get()
        self.intervalo = range(choice(range(4, linhas)))
        # self.cha = [Character(-a, self) for a in range(linhas - 2)]
        # self.cha.append(UltimoCharacter(-(len(self.cha)+1), self))
        self.cha = [Character(self) for x in range(linhas - 5)]
        self.cha += [PulseCharacter(self) for x in range(3)]
        shuffle(self.cha)
        for numero, character in enumerate(self.cha):
            character.cont = -numero
        self.cha.append(UltimoCharacter(self))
        self.cha[-1].cont = -(len(self.cha))
        self.ativo = ativo
        self.cor = cor

    def __iter__(self):
        return iter(self.cha)


class Architect:
    def __init__(self):
        self.c, l = get()
        self.colunas = [Coluna() for a in range(self.c)]

    def rain(self, stop=False):
        choice(self.colunas).ativo = True  # precisa iniciar a primeira
        colunas, linhas = get()
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
            if not choice(range(25)) == 1:
                choice(desativadas).__init__(True,)
            else:
                choice(desativadas).__init__(True, choice((4, 5)))

    def condicoes(self, colunas, linhas) -> bool:
        tupla =  ([a for a in get()] == [colunas, linhas],
                  [x for x in self.colunas if x.ativo])
        return all(tupla)


def main():
    texto_efeito_pausa('Conectando a matrix...')
    sleep(1)
    matrix = Architect()
    try:
        matrix.rain()
    except KeyboardInterrupt:
        matrix.rain(True)
    print('\n' * get()[1])
    texto_efeito_pausa(attr(0) + '\nDesconectado.')


if __name__ == '__main__':
    main()

# TODO: deixar rastro na tela como palavras escrito algo, exemplo: matrix
# TODO: fazer com que as colunas se iniciem em lugares aleatórios na tela.
# TODO: fazer com que algumas fileiras fiquem mais rápidas e outras mais lentas
# TODO: tentar trazer os caracteres katakanas novamente? (god mode programming)
