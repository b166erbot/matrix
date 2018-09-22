#the original matrix rain
from random import choice
from time import sleep
import re, sys, fire, pdb
from os import get_terminal_size, system as sy, name
from string import ascii_lowercase as string
from colored import fg, attr

itens = list(string)
#itens = [chr(i) for i in range(0x30a1, 0x30ff + 1)] # katakana characters
#itens += [str(a) for a in range(10)]
# os caracteres acima katakana não são usados pois eles tem tamanhos diferentes
# fazendo com que o matrix fique todo torto. :(

class Architect:
    """
    O arquiteto é o responsável pela construção da matrix, e esta é a 7 versão.
    """
    def __init__(self, recomeco = False):
        if not recomeco:
            print(fg('green'))
            self.range_len_itens = range(len(itens))
        print('\n'*100)
        self.linhas_matrix = []
        self.trava = False
        self.colunas, self.linhas = map(int,
            re.findall(r'\d+', str(get_terminal_size())))
        for a in range(self.linhas):
            self.linhas_matrix.append(' '*self.colunas)
        self.distancia_colunas = set(range(self.colunas))
        self.distancia_intervalos = list(range(24))
        self.colunas_intervalos = []
        self.stop_rain = False
        self.gerar_linhas()

    def sortear_colunas_intervalo(self, intervalo: list = False):
        """
        Função que sorteia quais colunas serão colocadas na tela, com intervalos
        de distância da coluna que será exibida.
        Intervalo recebe uma lista com Início e Fim da palavra.
        """
        self.colunas_intervalos = [[a[0], a[1]+1, a[2]+1]
            for a in self.colunas_intervalos]
        if not self.trava and not self.stop_rain:
            if intervalo:
                choice(list(range(*intervalo)))
            else:
                coluna = choice(list(self.distancia_colunas))
            intervalo_final = 0
            intervalo_inicial = -choice(self.distancia_intervalos)
            self.colunas_intervalos.append([coluna, intervalo_inicial,
                intervalo_final])
            self.colunas_intervalos.sort()
            self.distancia_colunas -= {coluna}
        if len(self.colunas_intervalos) >= int(self.colunas / 3):
            self.trava = True
        else:
            self.trava = False

    def gerar_linhas(self, intervalo = False):
        self.sortear_colunas_intervalo(intervalo)
        for linha in list(enumerate(self.linhas_matrix)):
            self.linhas_matrix[linha[0]] = self.refazer_strings(
                linha[1], linha[0])

    def refazer_strings(self, string: str, nlinha: int):
        # coluna_intervalo, formado por colunas[0], intervalos[1,2]
        if fg('white') in string:
            string = string.replace(fg('white'), '').replace(fg('green'), '')
        string = list(string)
        for a in self.colunas_intervalos:
            if a[1] > self.linhas:
                self.distancia_colunas.add(self.colunas_intervalos.pop(
                self.colunas_intervalos.index(a))[0])
            intervalo_inicial = self.filtro_zero(a[1])
            if nlinha not in range(intervalo_inicial,
                a[2]) and string[a[0]] != ' ':
                string[a[0]] = ' '
            elif nlinha in range(a[1], a[2]) and string[a[0]] == ' ':
                string[a[0]] = fg(
                'white') + itens[choice(self.range_len_itens)] + fg('green')
        return ''.join(string)

    def rastro(self, texto: str):
        for a in texto.split():
            for b in a:
                self.gerar_linhas([0, len(a)-1, texto]) #put the interval here

    def filtro_zero(self, x):
        if x < 0:
            return 0
        else:
            return x

    def displayAtual(self):
        return re.findall(r'\d+', str(get_terminal_size()))

    def rain(self):
        while True:
            display = [str(self.colunas), str(self.linhas)]
            while display == self.displayAtual() and self.colunas_intervalos:
                for a in list(enumerate(self.linhas_matrix)):
                    print(a[1])
                self.gerar_linhas()
                sleep(0.1)
            if self.stop_rain:
                break
            self.__init__(True)
            sleep(0.26)


def texto_efeito_pausa(texto: str, segundos: float = 0.1):
    for a in texto:
        print(a, end='')
        sys.stdout.flush()
        sleep(segundos)
    print()


def main():
    texto_efeito_pausa('Conectando a matrix...')
    sleep(1)
    try:
        matrix = Architect()
        matrix.rain()
    except KeyboardInterrupt:
        #print('\n'*50)
        matrix.stop_rain = True
        matrix.rain()
        texto_efeito_pausa(attr(0) + '\ndesconectado.')


if __name__ == '__main__':
    main()

"""eu sei que você está ai
eu posso sentir a sua presença
sei que está com medo
está com medo de nós
está com medo de mudar
eu não conheço o futuro
não vim lhe dizer como isso terminará
eu vim dizer, como vai começar
eu vou desligar o telefone e depois eu vou mostrar à essas pessoas
o que você não quer que elas vejam
eu vou mostrar um mundo, sem você
um mundo sem regras, nem controles, sem limites ou fronteiras
um mundo, onde qualquer coisa é possível
o que haverá depois, você vai decidir.
Thomas A. Anderson
"""
