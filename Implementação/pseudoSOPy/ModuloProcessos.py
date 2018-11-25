import operator

class Processo:
    def __init__ (self, processo):
        self.tempo_inicial  = int(processo[0])
        self.prioridade     = int(processo[1])
        self.tempo_cpu      = int(processo[2])
        self.blocos_mem     = int(processo[3])
        self.impressora     = int(processo[4])
        self.scanner        = int(processo[5])
        self.modem          = int(processo[6])
        self.disco          = int(processo[7])
        self.PID            = None

class GerenciadorProcessos:
    contPID = 0
    filaTempoReal   = []
    prioridade_1    = []
    prioridade_2    = []
    prioridade_3    = []
    filaProcessosUsuario = [] # Retirar
    filaProcessosProntos = []

    ''' Tira os processos da fila de pronto e insere na Fila de     '''
    ''' Processos de Prioridade ou na fila de Processos de Tempo Real  '''
    def separarProcesso(self, processo):
        if processo['prioridade'] == 0 and len(self.filaTempoReal) < 1000:
            self.filaTempoReal.append(processo)
        elif processo['prioridade'] == 1 and len(self.prioridade_1) < 1000:
            self.prioridade_1.append(processo)
        elif processo['prioridade'] == 2 and len(self.prioridade_2) < 1000:
            self.prioridade_2.append(processo)
        elif processo['prioridade'] == 3 and len(self.prioridade_3) < 1000:
            self.prioridade_3.append(processo)
        else:
            raise Exception("Capacidade maxima de processos atingida!!!! MAIOR QUE 1000!!!!")

    def escalonarProcesso(self, recursos, memoria):
        #seleciona o processo de maior prioridade
        if len(self.filaTempoReal) != 0:
            proc = self.filaTempoReal.pop(0)
            
            #checa disponibilidade de recursos
            if recursos.checarRecursos(proc) and memoria.checarMemoria(proc):
                # Se os recursos estao disponivel:
                # Atribui PID ao processo
                proc['PID'] = self.contPID
                print("Alocar memoria e alocar recursos")

                print("montar processo")
            else:
                # se nao disponivel, coloca o processo de volta na fila de pronto
                print("mandar processo para final da fila")

            self.filaProcessosProntos.insert(0, proc)
        elif len(self.prioridade_1) != 0:
            proc = self.prioridade_1.pop(0)
        elif len(self.prioridade_2) != 0:
            proc = self.prioridade_2.pop(0)
        elif len(self.prioridade_3) != 0:
            proc = self.prioridade_3.pop(0)
        else:
            ########## RETIRAR PRINT !!!!!!!!
            print("preencher else")






    def executarProcesso(self, recursos, memoria):
        self.escalonarProcesso(recursos, memoria)
        print("funcao executarProcesso")
