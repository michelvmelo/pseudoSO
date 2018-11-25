import threading
from itertools import groupby
from operator import itemgetter


class GerenciadorMemoria:
    def __init__(self):
        self.memoria = 1024*[-1]

        self.alocarMutex         = threading.Semaphore()
        self.desalocarMutex      = threading.Semaphore()

    # Checa se ha memoria disponivel para o processo
    def checarMemoria(self, processo):
        self.alocarMutex.acquire() # Semaforo que garante exclusao mutua
        self.desalocarMutex.acquire()
        offset = 0
        # Acha blocos continuos com marcados com mesmo PID ou com -1
        for k, g in groupby(enumerate(self.memoria), itemgetter(1)):
            bloco = map(itemgetter(1), g)
            #print map(itemgetter(1), g)
            if len(bloco) >= processo['blocos_mem'] and bloco[0] == -1:
                processo['offset'] = offset
                return True
            offset = offset + len(bloco)

        self.alocarMutex.release() # se nao tiver memoria p o processo
                                   # ele libera a escrita na memoria
        self.desalocarMutex.release()
        print("Nao ha memoria suficiente para executar o processo %s" %processo['PID'])
        return False

    def alocarMemoria(self, processo):
        # verificar como fechar a regiao critica
        PID     = processo['PID']
        offset  = processo['offset']
        blocos  = processo['blocos_mem']

        ini     = offset
        fim     = ini + processo['blocos_mem']

        self.memoria[ini:fim] = blocos*[PID]
        print(self.memoria)
        self.alocarMutex.release()
        self.desalocarMutex.release()

    def desalocaMemoria(self, processo):
        # verificar como fechar a regiao critica
        self.desalocarMutex.acquire()
        PID = processo['PID']
        ini = processo['offset']
        fim = ini + processo['blocos_mem']

        self.memoria[ini:fim] = blocos*[-1]
        self.desalocarMutex.release()
