from random import choice, choices, randint as ri
from time import sleep
from sys import stdout
from os import get_terminal_size as get
from string import ascii_lowercase as string
from colored import fg, attr
from functools import reduce


def texto_efeito_pausa(texto: str):
    for a in texto:
        print(a, end='')
        stdout.flush()
        sleep(0.04)
    print()


class Character:
    cores = {0: fg('grey_89'),
             1: fg('grey_66'),
             2: fg('white'),
             3: fg('green'),
             4: fg('yellow'),
             5: fg('red')}

    def __init__(self, cont, intervalo, coluna):
        col, self.lin = get()
        self.cont = cont
        self.intervalo = intervalo
        self.coluna = coluna
        self.character = self.cores[3] + choice(string)

    def __add__(self, other):
        string = ' '
        condicoes = [self.cont in self.intervalo, self.coluna.ativo]
        if self.cont < self.intervalo[-1] and self.coluna.ativo:
            string = self.character if all(condicoes) else ' '
        self.cont += 1
        self.novo_char()
        return other.__radd__(string)

    def __radd__(self, other):
        string = ' '
        condicoes = [self.cont in self.intervalo, self.coluna.ativo]
        if self.cont < self.intervalo[-1] and self.coluna.ativo:
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
        string = ' '
        condicoes = [self.cont in self.intervalo, self.coluna.ativo]
        if self.cont < self.intervalo[-1] and self.coluna.ativo:
            string = self.character if all(condicoes) else ' '
        else:
            self.coluna.ativo = False
        self.cont += 1
        self.novo_char()
        return other.__radd__(string)

    def __radd__(self, other):
        string = ' '
        condicoes = [self.cont in self.intervalo, self.coluna.ativo]
        if self.cont < self.intervalo[-1] and self.coluna.ativo:
            string = self.character if all(condicoes) else ' '
        else:
            self.coluna.ativo = False
        self.cont += 1
        self.novo_char()
        if isinstance(other, str):
            return other + string
        else:
            return other.character + string


class Coluna:
    def __init__(self, ativo=False, cor=3):
        c, l = get()
        u = choice(range(4, l))  # p, u = ri(0, l//3), ri(l//2, l)
        self.cha = [Character(-a, range(u), self) for a in range(l-2)]
        self.cha.append(UltimoCharacter(-(len(self.cha)+1), range(u), self))
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
        try:
            colunas, linhas = get()
            while list(get()) == [colunas, linhas]:
                while list(filter(lambda x: x.ativo, self.colunas)):  # por frames
                    if not stop:
                        self.sortear()
                    for b in range(choice(range(6))):  # por frame
                        for a in zip(*self.colunas):  # por linha
                            print(reduce(lambda x, y: x + y, a))
                        sleep(0.05)  # velocidade frames
                else:
                    break
        except KeyboardInterrupt:
            self.rain(True)

    def sortear(self):
        ativas = list(filter(lambda x: x.ativo, self.colunas))
        desativas = list(filter(lambda x: not x.ativo, self.colunas))
        if len(ativas) < self.c//3:
            if not choice(range(25)) == 1:
                choice(desativas).__init__(True)
            else:
                choice(desativas).__init__(True, choice((4, 5)))


def main():
    texto_efeito_pausa('Conectando a matrix...')
    sleep(1)
    print('\n' * 100)
    matrix = Architect()
    matrix.rain()
    texto_efeito_pausa(attr(0) + '\nDesconectado.')


if __name__ == '__main__':
    main()

# TODO: deixar rastro na tela como letras escrito algo, exemplo: matrix
# TODO: mudar o background(cor de fundo) da tela para amarelo?
# TODO: efeito alguém escrevendo
# TODO: todos estão começando do início da tela, fazer com que não
# TODO: fazer com que alguns caracteres no meio da coluna alterem
# TODO: fazer com que algumas fileiras fiquem mais rápidas e outras mais lentas
# TODO: tentar trazer os caracteres katakanas novamente?
