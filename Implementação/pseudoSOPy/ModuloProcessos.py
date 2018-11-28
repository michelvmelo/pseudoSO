import operator
import threading

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
        self.offset         = None
        self.PID            = None
        self.contInstrucao  = None


class GerenciadorProcessos:
    def __init__ (self):
        self.contPID = 0
        self.filaTempoReal   = []
        self.prioridade_1    = []
        self.prioridade_2    = []
        self.prioridade_3    = []
        self.filaProcessosProntos = []
        self.vcTempoReal = threading.Condition()
        self.executando = None

    def imprimirProcesso(self, processo):
        print('dispatcher =>')
        print('\tPID: {}'.format(processo['PID']))
        print('\toffset: {}'.format(processo['offset']))
        print('\tblocks: {}'.format(processo['blocos_mem']))
        print('\tpriority: {}'.format(processo['prioridade']))
        print('\ttime: {}'.format(processo['tempo_cpu']))
        print('\tprinters: {}'.format(processo['impressora']))
        print('\tscanners: {}'.format(processo['scanner']))
        print('\tmodems: {}'.format(processo['modem']))
        print('\tdrives: {}\n'.format(processo['disco']))

    ''' Tira os processos da fila de pronto e insere na Fila de     '''
    ''' Processos de Prioridade ou na fila de Processos de Tempo Real  '''
    def separarProcesso(self, processo):
        #print(processo)
        if (processo['prioridade'] == 0 and len(self.filaTempoReal) < 1000):
            self.filaTempoReal.append(processo)
        elif (processo['prioridade'] == 1 and len(self.prioridade_1) < 1000):
            prin("teste")
            self.prioridade_1.append(processo)
        elif (processo['prioridade'] == 2 and len(self.prioridade_2) < 1000):
            self.prioridade_2.append(processo)
        elif (processo['prioridade'] == 3 and len(self.prioridade_3) < 1000):
            self.prioridade_3.append(processo)
        else:
            raise Exception("Capacidade maxima de processos atingida!!!! MAIOR QUE 1000!!!!")

    def escalonarProcesso(self, recursos, memoria, arquivos):

        #seleciona o processo de maior prioridade
        if len(self.filaTempoReal) != 0:
            proc = self.filaTempoReal.pop(0)

            #checa disponibilidade de recursos
            if recursos.checarRecursos(proc) and memoria.checarMemoria(proc):
                # Se os recursos estao disponivel:
                # Atribui PID ao processo
                if proc['PID'] == None:
                    proc['PID'] = self.contPID
                    self.executando = proc
                    self.contPID += 1

                # Alocar gerenRecursos
                print("Alocando recursos...")
                recursos.alocarRecurso(proc)
                recursos.imprimirRecursos()
                print("Alocando memoria...")
                memoria.alocarMemoria(proc)

                print("montar processo")
                self.imprimirProcesso(proc)
                PID     = proc['PID']
                print('process {} =>'.format(proc['PID']))
                print('P{} STARTED'.format(proc['PID']))

                aux = arquivos.executaOperacao(proc)
                # Se nao tiver mais operacoes a executar mata o processo
                if not aux:
                    self.matarprocesso(recursos, memoria, proc)

            else:
                proc['tempo_inicial'] = proc['tempo_inicial'] + 1
                #self.filaProcessosProntos.append(proc)
                # se nao disponivel, coloca o processo de volta na fila de pronto
                #print("Nao ha recurso ou memoria para executar o processo!")
                print("mandar processo para final da fila")

            self.filaProcessosProntos.insert(0, proc)
        elif len(self.prioridade_1) != 0:
            proc = self.prioridade_1.pop(0)
        elif len(self.prioridade_2) != 0:
            proc = self.prioridade_2.pop(0)
        elif len(self.prioridade_3) != 0:
            proc = self.prioridade_3.pop(0)
        else:
            ########## RETIRAR PRINT !!!!!!!! Caso seja falso no loop
            print("preencher else")

    def matarprocesso(self, recursos, memoria, processo):
        aux = False
        if processo in self.filaProcessosProntos:
            self.filaProcessosProntos.remove(processo)
            aux = True
        if processo in self.filaTempoReal:
            self.filaTempoReal.remove(processo)
            aux = True
        if processo in self.prioridade_1:
            self.prioridade_1.remove(processo)
            aux = True
        if processo in self.prioridade_2:
            self.prioridade_2.remove(processo)
            aux = True
        if processo in self.prioridade_3:
            self.prioridade_3.remove(processo)
            aux = True
        if aux:
            recursos.desalocarRecurso(processo)
            memoria.desalocaMemoria(processo)

    def executarProcesso(self, recursos, memoria, arquivos):
        # Se ja existe um processo executando
        if self.executando is not None:
            aux = arquivos.executaOperacao(self.executando)
            # Se nao tiver mais operacoes a executar mata o processo
            if not aux:
                self.matarprocesso(recursos, memoria, self.executando)
        else:
            self.escalonarProcesso(recursos, memoria, arquivos)
