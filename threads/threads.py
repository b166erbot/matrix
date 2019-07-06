from threading import Thread
from time import sleep


class MultiThread:
    """ Classe gerenciadora de Threads. """

    def __init__(self, funcoes: list, queues: list):
        self.queues = queues
        zipped = zip(funcoes, queues)
        self.threads = [Thread(target=rodar, args=(funcao, queue), daemon=True)
                         for funcao, queue in zipped]

    def rodar(self):
        for thread in self.threads:
            thread.start()


def rodar(tarefa, queue):
    while True:
        # é obrigatório armazenar em uma variável ou condicionar com if a queue
        temp = queue.get()
        queue.put(tarefa())
        queue.task_done()  # task_done não mata a tarefa?
