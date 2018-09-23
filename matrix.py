#the original matrix rain
from random import choice
from time import sleep
import re, sys, fire
from os import get_terminal_size
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
        print('\n'*30)
        self.colunas, self.linhas = map(int,
            re.findall(r'\d+', str(get_terminal_size())))
        self.minCol = int(self.colunas/5)
        self.maxCol = int(self.colunas/3)
        self.linhas_matrix, self.colunas_intervalos = [], []
        for a in range(self.linhas):
            self.linhas_matrix.append(' '*self.colunas)
        self.trava = False
        self.stop_rain = False
        self.distancia_colunas = list(range(self.colunas))
        self.distancia_intervalos = list(range(24))
        self.gerar_linhas()

    def sortear_colunas_intervalo(self, rastro: list = False) -> list:
        """
        Função que sorteia quais colunas serão colocadas na tela, com intervalos
        de distância da coluna que será exibida.
        """
        coluna = False
        sortear = False
        contagem = len(self.colunas_intervalos)
        if not self.trava and not self.stop_rain:
            if contagem > self.minCol:
                sortear = True
            if rastro:
                coluna = rastro[1]
            else:
                if sortear:
                    if choice([0, 1]):
                        coluna = choice(self.distancia_colunas)
                else:
                    coluna = choice(self.distancia_colunas)
            intervalo_final = 0
            intervalo_inicial = -choice(self.distancia_intervalos)
            return coluna, [coluna, intervalo_inicial, intervalo_final]
        return []

    def gerar_linhas(self, rastro: list = False):
        self.colunas_intervalos = [[a[0], a[1]+1, a[2]+1]
            for a in self.colunas_intervalos]
        self.add_remove_colunas(*self.sortear_colunas_intervalo(rastro))
        self.trava = self.des_travar()
        for linha in list(enumerate(self.linhas_matrix)):
            self.linhas_matrix[linha[0]] = self.refazer_strings(*linha, rastro)

    def refazer_strings(
    self, nlinha: int, string: str, rastro: str=False) -> str:
        """
        Função que refatora a string ordenando as palavras de acordo com o
        intervalo de distância imposto e colore as letras de acordo com o filme
        geradas no intervalo.
        """
        # coluna_intervalo, formado por colunas[0], intervalos[1,2]
        if fg('white') in string:
            string = string.replace(fg('white'), '').replace(fg('green'), '')
        string = list(string)
        for a in self.colunas_intervalos:
            if a[1] > self.linhas:
                self.add_remove_colunas(a)
            intervalo_inicial = self.filtro_zero(a[1])
            condicao1 = nlinha not in range(intervalo_inicial, a[2])
            if condicao1 and string[a[0]] != ' ':
                string[a[0]] = ' '
            elif rastro and condicao1 and string[a[0]] == rastro[0]:
                pass
            elif nlinha in range(*a[1:]) and string[a[0]] == ' ':
                if not rastro:
                    letra = itens[choice(self.range_len_itens)]
                else:
                    letra = rastro[0]
                string[a[0]] = fg('white') + letra + fg('green')
        return ''.join(string)

    def rastro(self, texto: str) -> list:
        #distancia com bug nos tamanhos
        #não está mantendo o rastro, verificar
        #rastro = palavra, coluna_correta
        textoRecortado = [texto[a*80:(a+1)*80] for a in range(len(texto)//80+1)]
        for recorte in textoRecortado:
            texto = list(recorte[0])
            for b in recorte[0]:
                indice = choice(range(len(texto)))
                letra = texto.pop(indice)
                self.gerar_linhas([letra, indice])

    def des_travar(self):
        if len(self.colunas_intervalos) >= self.maxCol:
            return True
        return False

    def imprimir_na_tela(self): #vai receber mais algo como argumento
        pass

    def filtro_zero(self, x):
        if x < 0:
            return 0
        return x

    def displayAtual(self):
        return re.findall(r'\d+', str(get_terminal_size()))

    def add_remove_colunas(self, x=False, lista=False):
        """
        Função que adiciona ou remove colunas que serão exibidas na tela.
        """
        if x:
            if lista:
                #print(x)
                self.distancia_colunas.remove(x)
                self.colunas_intervalos.append(lista)
                self.colunas_intervalos.sort()
            else:
                self.distancia_colunas.append(self.colunas_intervalos.pop(
                self.colunas_intervalos.index(x))[0])


    def rain(self, texto=False):
        while True:
            display = [str(self.colunas), str(self.linhas)]
            while display == self.displayAtual() and self.colunas_intervalos:
                for a in list(enumerate(self.linhas_matrix)):
                    print(a[1])
                if not texto:
                    self.gerar_linhas()
                else:
                    self.rastro(texto)
                sleep(0.1)
            if self.stop_rain:
                break
            self.__init__(True)
            sleep(0.26)


def texto_efeito_pausa(texto: str):
    for a in texto:
        print(a, end='')
        sys.stdout.flush()
        sleep(0.04)
    print()


def main():
    texto_efeito_pausa('Conectando a matrix...')
    sleep(1)
    matrix = Architect()
    try:
        matrix.rain()
    except KeyboardInterrupt:
        matrix.stop_rain = True
        while matrix.colunas_intervalos:
            try:
                matrix.rain()
            except:
                pass
        texto_efeito_pausa(attr(0) + '\ndesconectado.')

if __name__ == '__main__':
    main()

#bug ao redimencionar a tela depois que eu aperto ctrl + c

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
