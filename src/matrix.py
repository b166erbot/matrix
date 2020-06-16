import curses
from os import get_terminal_size as get_size
from time import sleep
from typing import NoReturn, Iterable, Tuple, List, Callable
from random import randint, choice, shuffle
from string import ascii_lowercase as string
from itertools import cycle, chain
from functools import reduce, namedtuple
from operator import add

from .cores import cor


dados = namedtuple(
    'dados', ['no_intervalo', 'desativar', 'maior_que_intervalo',
    'local_exato_caracter', 'cor', 'ativa', 'tela']
)


def texto_efeito_pausa(texto: str) -> NoReturn:
    """Função que imprime um texto como se alguém estivesse digitando."""
    for letra in texto:
        print(letra, end='', flush=True)
        sleep(0.04)
    print()


class Caracter:
    """Classe que representa um caracter qualquer."""

    def __init__(self, dados: namedtuple) -> NoReturn:
        self._caracter = choice(string)
        self._dados = dados

    def __repr__(self) -> str:
        return f"{self._caracter}"

    def __str__(self) -> str:
        return self._caracter

    def exibir(self, numero_linha: int, numero_coluna: int) -> NoReturn:
        """Método que posiciona todos os caracteres na tela."""
        caracter = self._obter_caracter()
        cor = self._obter_cor()
        if self._dados.ativa():
            self._dados.tela.addch(numero_linha, numero_coluna, caracter, cor)

    def _obter_caracter(self) -> str:
        """Método que retorna o caracter."""
        if self._dados.no_intervalo(self):
            caracter = self._caracter
        else:
            caracter = ' '
        return caracter

    def _obter_cor(self) -> int:
        """Método que retorna a cor."""
        local = int(self._dados.local_exato_caracter(self))
        if local in [1, 2]:
            cor_ =  cor('white')
        elif local == 3:
            cor_ =  cor('gray')
        else:
            cor_ =  self._dados.cor()
        return cor_


class UltimoCaracter(Caracter):
    """Classe que representa o último caracter."""

    def exibir(self, numero_linha: int, numero_coluna: int) -> NoReturn:
        super().exibir(numero_linha, numero_coluna)
        if self._dados.maior_que_intervalo(self):
            self._dados.desativar()


class PulsarCaracter(Caracter):
    """docstring for PulsarCaracter"""

    def _obter_caracter(self) -> str:
        """Método que retorna o caracter."""
        caracter = choice(string) if self._dados.no_intervalo(self) else ' '
        return caracter

    def _obter_cor(self) -> int:
        """Método que retorna a cor."""
        return cor('white')


class Coluna:
    """Classe que armazena todos os caracteres de uma coluna."""

    def __init__(self, tamanho: int, tela) -> NoReturn:
        self._tamanho = tamanho  # necessário para reiniciar.
        self._tela = tela  # necessário para reiniciar.
        self._intervalo = [- randint(7, tamanho), -2]
        self._cor = cor('green')
        dados_ = dados(
            self._no_intervalo, self.desativar, self.maior_que_intervalo,
            self.local_exato_caracter, self.cor, self.ativa, tela
        )
        # tamanho -1 no mínimo obrigatório abaixo. motivo: FixBug
        caracteres = list(map(
            lambda x: Caracter(dados_), range(tamanho - int(tamanho / 4))
        ))
        caracteres = caracteres + list(map(
            lambda x: PulsarCaracter(dados_), range(int(tamanho / 5))
        ))  # tamanho / 5
        shuffle(caracteres)
        self._caracteres = list(chain(caracteres, [UltimoCaracter(dados_)]))
        self._ativa = False
        self._pulo = 1

    def __repr__(self) -> str:
        return f"{self._caracteres[:5]}..."

    def __iter__(self) -> Iterable[Caracter]:
        return iter(self._caracteres)

    def andar(self) -> NoReturn:
        """Método que faz a coluna andar."""
        self._intervalo[0] += self._pulo
        self._intervalo[1] += self._pulo

    def local_exato_caracter(self, caracter: Caracter) -> int:
        """Método que retorna o local do caracter perante o tamano da coluna."""
        local = self._caracteres.index(caracter)
        return self._intervalo[1] - local

    def maior_que_intervalo(self, caracter: Caracter) -> bool:
        """Método que verifica se o local do caracter é maior que a coluna."""
        local = self._caracteres.index(caracter)
        return self._intervalo[0] > local

    def _no_intervalo(self, caracter: Caracter) -> bool:
        """Método que verifica se o caracter está no intervalo da coluna."""
        local = self._caracteres.index(caracter)
        distancia = map(int, self._intervalo)
        return True if local in range(*distancia) else False

    def desativar(self) -> NoReturn:
        """Método que desativa a coluna."""
        self.__init__(self._tamanho, self._tela)
        self._ativa = False

    def definir_status(self, status: bool) -> NoReturn:
        """Método que define o status da coluna."""
        self._ativa = status

    def ativa(self) -> bool:
        """Método que verifica se a coluna está ativa."""
        return self._ativa

    def exibir(self, numero_coluna: int) -> NoReturn:
        """Método que posiciona todos os caracteres na tela."""
        for numero_linha, caracter in enumerate(self):
            caracter.exibir(numero_linha, numero_coluna)

    def definir_cor(self, cor) -> NoReturn:
        """Método que define a cor da coluna."""
        self._cor = cor

    def cor(self) -> int:
        """Método que retorna a cor da coluna."""
        return self._cor

    def definir_instabilidade(self) -> NoReturn:
        self._pulo = choice([0.5, 2])


class Arquiteto:
    """Classe que gerencia todas as colunas na tela."""

    def __init__(self, tela) -> NoReturn:
        self._tela = tela
        lin, col = tela.getmaxyx()
        self._lin = lin
        self._colunas = list(map(
            lambda linhas: Coluna(linhas, tela), [lin] * (col - 1)
        ))
        self.continue_ = True

    def _exibir(self) -> NoReturn:
        """Método que exibe todos os caracteres das colunas."""
        for numero_coluna, coluna in enumerate(self._colunas):
            coluna.exibir(numero_coluna)

    def _andar(self) -> NoReturn:
        """Método que faz todas as colunas andarem."""
        colunas = filter(lambda x: x.ativa(), self._colunas)
        for coluna in colunas:
            coluna.andar()

    def _ativar_colunas(self) -> NoReturn:
        """Método que ativa as colunas desativadas."""
        tamanho = curses.getsyx()[1]
        colunas_desativadas = list(filter(
            lambda x: not x.ativa(), self._colunas
        ))
        if len(colunas_desativadas) > tamanho/3 and self.continue_:
            choice(colunas_desativadas).definir_status(True)

    def _desativar_todas_colunas(self) -> NoReturn:
        """Método que desativa todas as colunas."""
        for coluna in self._colunas:
            coluna.desativar()

    def _sortear_coloridas(self) -> NoReturn:
        """Método que seleciona e define a cor de uma coluna."""
        if choice(range(20)) == 1:  # 20
            desativadas = list(filter(lambda x: not x.ativa(), self._colunas))
            cor_ = cor(choice(['orange', 'red']))
            choice(desativadas).definir_cor(cor_)

    def _sortear_instaveis(self) -> NoReturn:
        if choice(range(4)) == 1: # 5
            desativadas = list(filter(lambda x: not x.ativa(), self._colunas))
            choice(desativadas).definir_instabilidade()

    def _conectado(self, tamanho_anterior: int) -> bool:
        """Método que verifica se o programa ainda pode continuar rodando."""
        igual = list(get_size()) == tamanho_anterior
        ativas = len(list(filter(lambda x: x.ativa(), self._colunas)))
        return igual and (ativas > 0)

    def rain(self) -> NoReturn:
        """Método que roda todo o efeito."""
        tamanho_anterior = list(get_size())
        self._ativar_colunas()  # é obrigatório que uma coluna esteja ativa.
        while self._conectado(tamanho_anterior):
            self._andar()
            self._ativar_colunas()
            self._sortear_coloridas()
            self._sortear_instaveis()
            self._exibir()
            self._tela.refresh()
            sleep(0.04)  # 0.05
        self._desativar_todas_colunas()
        self._tela.erase()
        self._tela.refresh()


def configurar(tela) -> NoReturn:
    """Função que faz as configurações iniciais."""
    curses.curs_set(0)  # oculta o pipe
    curses.noecho()
    curses.start_color()
    curses.use_default_colors()
    for x, y in enumerate(range(10), 1):
        curses.init_pair(x, y, -1)


def main() -> NoReturn:
    """Função principal."""

    texto_efeito_pausa('Conectando a matrix...')
    sleep(1)
    try:
        curses.initscr()
        while True:
            colunas, linhas = get_size()
            tela = curses.newwin(linhas + 1, colunas + 1)  # correção de bug
            configurar(tela)
            matrix = Arquiteto(tela)
            matrix.rain()
    except KeyboardInterrupt:
        matrix.continue_ = False
        matrix.rain()
    finally:
        curses.endwin()
    texto_efeito_pausa('\nDesconectado.')

# addstr, addch -> linhas(y), colunas(x), string, cor
