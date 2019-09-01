from random import choice, choices, randint as ri
from time import sleep
from sys import stdout
from os import get_terminal_size as get, system as sy
from string import ascii_lowercase as string
from colored import fg, attr
from functools import reduce
from cython import boundscheck, wraparound
# from threads import CadeiaCaracteres


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

    def __init__(self, arquiteto, coluna, cont, intervalo):
        self.arquiteto = arquiteto
        col, self.lin = get()
        self.cont = cont
        self.intervalo = intervalo
        self.coluna = coluna
        self.character = self.cores[3] + choice(string)
        if self.coluna in self.arquiteto.desativadas:
            index = self.arquiteto.desativadas.index(self.coluna)
            self.arquiteto.desativadas.pop(index)
        self.arquiteto.ativas.append(self.coluna)

    def __add__(self, other):
        string = ' '
        condicoes = [self.cont in self.intervalo,
                     self.coluna in self.arquiteto.ativas]
        if self.cont < self.intervalo[-1] and condicoes[1]:
            string = self.character if all(condicoes) else ' '
        self.cont += 1
        self.novo_char()
        return other.__radd__(string)

    def __radd__(self, other):
        string = ' '
        condicoes = [self.cont in self.intervalo,
                     self.coluna in self.arquiteto.ativas]
        if self.cont < self.intervalo[-1] and condicoes[1]:
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

    def novo_char(self):
        if self.cont in range(3):
            self.character = self.cores[self.cont] + choice(string)
        else:
            self.character = self.cores[self.coluna.cor] + self.character[-1]


class UltimoCharacter(Character):
    def __add__(self, other):
        string = ' '
        condicoes = [self.cont in self.intervalo,
                     self.coluna in self.arquiteto.ativas]
        if self.cont < self.intervalo[-1] and condicoes[1]:
            string = self.character if all(condicoes) else ' '
        else:
            if condicoes[1]:
                index = self.arquiteto.ativas.index(self.coluna)
                self.arquiteto.ativas.pop(index)
            self.arquiteto.desativadas.append(self.coluna)
        self.cont += 1
        self.novo_char()
        return other.__radd__(string)

    def __radd__(self, other):
        string = ' '
        condicoes = [self.cont in self.intervalo,
                     self.coluna in self.arquiteto.ativas]
        if self.cont < self.intervalo[-1] and condicoes[1]:
            string = self.character if all(condicoes) else ' '
        else:
            if condicoes[1]:
                index = self.arquiteto.ativas.index(self.coluna)
                self.arquiteto.ativas.pop(index)
            self.arquiteto.desativadas.append(self.coluna)
        self.cont += 1
        self.novo_char()
        if isinstance(other, str):
            return other + string
        else:
            return other.character + string


class Coluna:
    def __init__(self, arqui, ativo=False, cor=3):
        c, l = get()
        u = choice(range(4, l))  # p, u = ri(0, l//3), ri(l//2, l)
        self.cha = [Character(arqui, self, -a, range(u)) for a in range(l-2)]
        self.cha.append(
            UltimoCharacter(arqui, self, -(len(self.cha)+1), range(u)))
        self.cor = cor

    def __iter__(self):
        return iter(self.cha)


class Architect:
    def __init__(self):
        self.c, l = get()
        self.ativas = []
        self.desativadas = []
        self.colunas = []
        for a in range(self.c):
            coluna = Coluna(self)
            self.desativadas.append(coluna)
            self.colunas.append(coluna)

    def rain(self, stop=False):
        # choice(self.colunas).ativo = True  # precisa iniciar a primeira
        choice(self.desativadas).__init__(self, True)
        colunas, linhas = get()
        try:
            while self.condicoes(colunas, linhas):  # por frames
                if not stop:
                    self.sortear()
                for b in range(choice(range(1, 5))):  # por frame
                    sy('clear')
                    for a in zip(*self.colunas):  # por linha
                        print(reduce(lambda x, y: x + y, a))
                    sleep(0.05)  # velocidade frames
        except KeyboardInterrupt:
            self.rain(True)

    @boundscheck(False)
    @wraparound(False)
    def sortear(self):
        if self.c - len(self.desativadas) < self.c//3:
            if not choice(range(25)) == 1:
                choice(self.desativadas).__init__(self, True)
            else:
                choice(self.desativadas).__init__(self, True, choice((4, 5)))

    def condicoes(self, colunas, linhas):
        tupla =  ([a for a in get()] == [colunas, linhas],
                  self.ativas)
        return all(tupla)


def main():
    texto_efeito_pausa('Conectando a matrix...')
    sleep(1)
    print('\n' * 100)
    matrix = Architect()
    matrix.rain()
    texto_efeito_pausa(attr(0) + '\nDesconectado.')


if __name__ == '__main__':
    # main()
    raise Exception('Do not execute this script!')

# TODO: botar as colunas para se auto ativarem daqui a um certo tempo?
# TODO: deixar rastro na tela como letras escrito algo, exemplo: matrix
# TODO: mudar o background(cor de fundo) da tela para amarelo?
# TODO: todos estão começando do início da tela, fazer com que não
# TODO: fazer com que alguns caracteres no meio da coluna alterem
# TODO: fazer com que algumas fileiras fiquem mais rápidas e outras mais lentas
# TODO: fazer com que as colunas se desativem e vão para uma lista de desativa.?
# TODO: tentar trazer os caracteres katakanas novamente?


from queue import Queue


class CadeiaCaracteres:
    """ Classe gerenciadora de caracteres. """

    def __init__(self):
        self.queue = Queue()
        self.thread = Thread(target=self.tarefa, daemon=True)

    def rodar(self):
        self.thread.start()

    def tarefa(self):
        while True:
            próximo = self.queue.get()
            self.queue.put()
