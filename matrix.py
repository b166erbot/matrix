from random import choice
from time import sleep
import sys
from os import get_terminal_size as get_size
from string import ascii_lowercase as string
from colored import fg, attr


class Architect:

    def __init__(self, recomeco=False):
        if not recomeco:
            print(fg('green'))
        print('\n'*50)
        self.colunas, self.linhas = list(get_size())
        self.minCol, self.maxCol = int(self.colunas/3), int(self.colunas/2)
        self.linhas_matrix, self.local = [], dict()
        for a in range(self.linhas):
            self.linhas_matrix.append(' ' * self.colunas)
        self.parar, self.trava = False, False

    def _gerar_linhas(self):
        # por em outro lugar a linha abaixo, self.trava
        self.trava = (True if len(self.local) >= self.maxCol
                      or self.parar else False)
        for a in self.local.copy():
            self.local[a] = [n + 1 for n in self.local[a]]
            if self.local[a][0] == self.linhas:
                self.local.pop(a)
        if not self.trava:
            if len(self.local) >= self.minCol:
                # inserir colunas, sortear colunas à acrecentar
                if choice([0, 1]):
                    nova_lista = list(filter(self._notIn, range(self.colunas)))
                    coluna = choice(nova_lista)
                    self.local[coluna] = [-choice(range(24)), 0]
                    # se a localização no indice 0 for == 24, delete.
                    # onde vai deletar é que eu não sei.
            elif len(self.local) >= 0:
                # insirir colunas
                nova_lista = list(filter(self._notIn, range(self.colunas)))
                coluna = choice(nova_lista)
                self.local[coluna] = [-choice(range(24)), 0]

    def _refazer_strings(self):
        # bug, todas as caracteres estão mudando.
        for linha in range(0, self.linhas):
            temp = self.linhas_matrix[linha].replace(fg('white'), '')
            self.linhas_matrix[linha] = temp.replace(fg('green'), '')
            texto = ''
            for n in range(self.colunas):
                if n in self.local and linha in range(*self.local[n]):
                    texto += self.linhas_matrix[linha][n]
                elif n in self.local and linha == self.local[n][1]:
                    texto += fg('white') + choice(string) + fg('green')
                else:
                    texto += ' '
            self.linhas_matrix[linha] = texto

    def _notIn(self, item):
        return item not in self.local

    def rain(self):
        try:
            self._gerar_linhas()
            while self.local:
                for linha in self.linhas_matrix:
                    print(linha)
                self._gerar_linhas()
                self._refazer_strings()
                sleep(0.1)
        except KeyboardInterrupt:
            self.parar = True
            self.rain()


if __name__ == '__main__':
    matrix = Architect()
    matrix.rain()

