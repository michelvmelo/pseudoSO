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
        self.contRetorno    = 0


class GerenciadorProcessos:
    def __init__ (self):
        self.contPID = 0
        self.filaTempoReal   = []
        self.prioridade_1    = []
        self.prioridade_2    = []
        self.prioridade_3    = []
        self.filaProcessosProntos = []
        self.listaProcessos = []
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
            self.prioridade_1.append(processo)
        elif (processo['prioridade'] == 2 and len(self.prioridade_2) < 1000):
            self.prioridade_2.append(processo)
        elif (processo['prioridade'] == 3 and len(self.prioridade_3) < 1000):
            self.prioridade_3.append(processo)
        else:
            #print(processo)
            print("Capacidade maxima de processos atingida!!!! MAIOR QUE 1000!!!!")

    def criarProcesso(self, recursos, memoria, arquivos, proc):
        if recursos.checarRecursos(proc) and memoria.checarMemoria(proc):
            # Se os recursos estao disponivel:
            # Atribui PID ao processo
            if proc['PID'] == None:
                proc['PID'] = self.contPID
                self.executando = proc
                self.contPID += 1

            self.filaProcessosProntos = [x for x in self.filaProcessosProntos if x != proc]
            # Alocar gerenRecursos
            #print("Alocando recursos...")
            recursos.alocarRecurso(proc)
            #recursos.imprimirRecursos()
            #print("Alocando memoria...")
            memoria.alocarMemoria(proc)

            #print("montar processo")
            self.imprimirProcesso(proc)
            PID     = proc['PID']
            print('process {} =>'.format(proc['PID']))
            print('P{} STARTED'.format(proc['PID']))

            arquivos.executaOperacao(recursos, memoria, self, proc)
            # Se nao tiver mais operacoes a executar mata o processo
            return True


        else:
            proc['tempo_inicial'] = proc['tempo_inicial'] + 1

            # Verifica as condicoes da indisponibilidade de recurso
            impressora      = proc['impressora']
            scanner         = proc['scanner']
            modem           = proc['modem']
            disco           = proc['disco']
            boolImpressora  = impressora > 2 or impressora < 0
            boolScanner     = scanner != 1
            boolModem       = modem   != 1
            boolDisco       = disco > 2 or disco < 0
            # Verifica as condicoes da indisponibilidade de memoria
            if proc['prioridade'] == 0 and proc['blocos_mem'] > 64:
                #self.filaTempoReal.remove(proc)
                print 'O processo requer um tamanho de memoria maior que o disponivel.(Esse processo de nucleo nao sera executado nunca)\n'

            elif proc['prioridade'] != 0 and proc['blocos_mem'] > 960:
                #self.filaTempoReal.remove(proc)
                print 'O processo requer um tamanho de memoria maior que o disponivel.(Esse processo de usuario nao sera executado nunca)\n'

            elif boolImpressora or boolScanner or boolModem or boolDisco:
                print 'Os recursos solicitados pelo processo nao existem no sistema!\n'

            else:
                # Se nao existe espacao mas ele cabe na gerenMemoria
                # Manda o processo para o fim da fila
                #self.filaTempoReal.remove(proc)
                if proc['PID'] == None:
                    proc['PID'] = self.contPID
                    self.executando = proc
                    self.contPID += 1
                if proc['contRetorno'] < 2:
                    proc['contRetorno'] += 1
                    self.filaProcessosProntos.append(proc)
                else:
                    self.filaProcessosProntos.remove(proc)
                return True
            self.filaProcessosProntos.remove(proc)
            return False


    def enviarFimFila(self, recursos, memoria, processo):
        self.desalocar(recursos, memoria, processo)
        self.filaProcessosProntos.append(processo)

    def desalocar(self, recursos, memoria, processo):

        self.executando = None
        if processo['offset'] != None:
            memoria.desalocaMemoria(processo)
            processo['offset'] = None
        recursos.desalocarRecurso(processo)
