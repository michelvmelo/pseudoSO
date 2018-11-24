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

class GerenciadorProcessos:
    PID = 0
    filaTempoReal   = []
    prioridade_1    = []
    prioridade_2    = []
    prioridade_3    = []
    filaProcessosUsuario = []
    filaProcessosProntos = []

    ''' Tira os processos da fila de pronto e insere na Fila de     '''
    ''' Processos de Usuario ou na fila de Processos de Tempo Real  '''
    def separarProcesso(self):

        if(self.filaProcessosProntos[0]['prioridade'] == 0) and (len(self.filaTempoReal) < 1000):
            proc = self.filaProcessosProntos.pop(0)
            self.filaTempoReal.append(proc)

        print(self.filaTempoReal)

    def novoProcesso(self, processo):
