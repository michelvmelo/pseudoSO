import threading

class GerenciadorMemoria:
    def __init__(self):
        self.memoria = 1024*[-1]

        self.alocarMutex         = threading.Semaphore()
        self.desalocarMutex      = threading.Semaphore()
    # Checa se ha memoria disponivel para o processo
    def checarMemoria(self, processo):

        offset = 0
        if processo['prioridade'] == 0:
            #Implementar forma achar bloco continuo
            cont = len([x for x in self.memoria if x == -1])
            if processo['blocos_mem'] <= cont:
                return True
            else:
                return  False
        else:
            #Implementar forma achar bloco continuo
            cont = len([x for x in self.memoria if x == -1])
            if processo['blocos_mem'] <= cont:
                return True
            else:
                return  False

    def alocarMemoria(self, processo):
        # verificar como fechar a região critica
        self.alocarMutex.acquire()
        PID = processo['PID']
        blocos = processo['blocos_mem']
        offset = 0 # falta achar offset correto
        ini = offset
        fim = ini + processo['blocos_mem']
        processo['offset'] = 0 # fornecer o offset correto

        self.memoria[ini:fim] = blocos*[PID]
        print(self.memoria)
        self.alocarMutex.release()

    def desalocaMemoria(self, processo):
        # verificar como fechar a região critica
        self.desalocarMutex.acquire()
        PID = processo['PID']
        ini = processo['offset']
        fim = ini + processo['blocos_mem']

        self.memoria[ini:fim] = blocos*[-1]
        self.desalocarMutex.release()
