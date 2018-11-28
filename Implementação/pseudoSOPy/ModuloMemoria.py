from itertools import groupby
from operator import itemgetter


class GerenciadorMemoria:
    def __init__(self):
        self.memoria = 1024*[-1]

    # Checa se ha memoria disponivel para o processo
    def checarMemoria(self, processo):


        memReal = [x for x in self.memoria[0:64]]
        memUser = [x for x in self.memoria[64:1024]]
        #se for processo do sistema
        if processo['prioridade'] == 0:
            offset = 0
            # Acha blocos continuos com marcados com mesmo PID ou com -1
            for k, g in groupby(enumerate(memReal), itemgetter(1)):
                bloco = map(itemgetter(1), g)
                if len(bloco) >= processo['blocos_mem'] and bloco[0] == -1:
                    processo['offset'] = offset
                    return True
                offset = offset + len(bloco)
        else:
            #Se for processo de usuario
            offset = 64
            # Acha blocos continuos com marcados com mesmo PID ou com -1
            for k, g in groupby(enumerate(memUser), itemgetter(1)):
                bloco = map(itemgetter(1), g)
                #print map(itemgetter(1), g)
                if len(bloco) >= processo['blocos_mem'] and bloco[0] == -1:
                    processo['offset'] = offset
                    return True
                offset = offset + len(bloco)

        print("Nao ha memoria suficiente para executar o processo")
        return False

    def alocarMemoria(self, processo):
        # verificar como fechar a regiao critica
        PID     = processo['PID']
        offset   = processo['offset']
        blocos   = processo['blocos_mem']

        ini     = offset
        fim     = ini + processo['blocos_mem']

        self.memoria[ini:fim] = blocos*[PID]


    def desalocaMemoria(self, processo):
        PID = processo['PID']
        ini = processo['offset']
        fim = ini + processo['blocos_mem']
        self.memoria[ini:fim] = processo['blocos_mem']*[-1]
