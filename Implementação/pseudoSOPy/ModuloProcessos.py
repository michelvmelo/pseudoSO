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


class GerenciadorProcessos:
    def __init__ (self):
        self.contPID = 0
        self.filaTempoReal   = []
        self.prioridade_1    = []
        self.prioridade_2    = []
        self.prioridade_3    = []
        self.filaProcessosUsuario = [] # Retirar
        self.filaProcessosProntos = []
        self.vcTempoReal = threading.Condition()
        self.executando = {}

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
                    self.contPID += 1

                # Alocar gerenRecursos
                print("Alocando recursos...")
                recursos.alocarRecurso(proc)
                print("Alocando mamoria...")
                memoria.alocarMemoria(proc)

                print("montar processo")
                self.imprimirProcesso(proc)

                #executar Processo
                #operacoes = [x for x in arquivos.listaOperacoes if x['idProcesso'] == proc['PID']]
                arquivos.executaOperacao(proc)

                recursos.desalocarRecurso(proc)
                memoria.desalocaMemoria(proc)
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


    def executarProcesso(self, recursos, memoria, arquivos):
        self.escalonarProcesso(recursos, memoria, arquivos)
        print("funcao executarProcesso")
