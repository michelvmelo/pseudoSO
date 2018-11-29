# -*- coding: utf-8 -*-
from itertools import groupby
from operator import itemgetter

class Arquivo:
    def __init__(self, arquivo, ID = None):
        self.nome               = arquivo[0]
        self.primeiroBloco      = int(arquivo[1])
        self.quantidadeBlocos   = int(arquivo[2])
        self.ID = ID

class Operacao:
    def __init__(self, info):
        self.idOperacao         = None
        self.idProcesso         = int(info[0])
        self.codOperacao        = int(info[1])
        self.nomeArquivo        = info[2]
        self.controlador        = 0
        if (self.codOperacao == 0):
            self.numeroBlocos = int(info[3])
        else:
            self.numeroBlocos = None

class GerenciadorArquivos:
    numeroBlocos = 0
    numeroSegmentos = 0
    listaArquivos = []
    listaOperacoes = []
    disco = []
    log = []
    arquivos = []

    def imprimirDisco(self):
        str = "| "
        for n in self.disco:
            str += "{} ".format(n)
        str += "|"
        print str
    def numerarOperacoes(self):
        x = 1
        for op in self.listaOperacoes:
            op['idOperacao'] = x
            x +=1

    ''' Inicializa o disco com as informacos de entrada'''
    def inicializarDisco(self):
        # criando um disco com a quantidade de blocos fornecidos na entrada
        self.disco = [-1 for i in range(self.numeroBlocos)]
        for arquivos in self.listaArquivos:
            # Preenche os blocos do disco com o nome dos arquivos de entrada correspondente
            self.disco[arquivos['primeiroBloco']:arquivos['primeiroBloco'] + arquivos['quantidadeBlocos']] = arquivos['quantidadeBlocos'] *[arquivos['nome']]

    def executaOperacao(self, gerenProcesso, processo):
        #SELECIONA OPERACOES DO PROCESSO
        ops = [op for op
                in self.listaOperacoes
                if op['idProcesso'] == processo['PID']
              ]

        if ops:
            if processo['contInstrucao'] is None:
                processo['contInstrucao'] = 1
            else:
                processo['contInstrucao'] += 1
            print('P{} instruction {}'.format(processo['PID'], processo['contInstrucao']))

            # Se é opercao de criar arquivo
            op0 = [op for op in ops if op['codOperacao'] == 0]
            op1 = [op for op in ops if op['codOperacao'] == 1]
            ####### OPERACAO PARA CRIAR ARQUIVO ###########
            if op0:

                #VERIFICAR CONDICOES SE EH MAIOR Q TODOS OS BLOCOS DO DISCO
                offset       = 0
                execOp       = False
                op           = op0.pop(0)
                nomeArquivo  = op['nomeArquivo']
                numeroBlocos = op['numeroBlocos']
                existeArq = [x for x in self.listaArquivos if x['nome'] == nomeArquivo]

                # Verifica se o numero de blocos do arquivo no eh maior que os blocos do disco
                if numeroBlocos > len(self.disco):
                    self.listaOperacoes.remove(op)
                    print 'Operação {} => Falha'.format(op['idOperacao'])
                    print 'O numero de blocos solicitados é maior que o existente em disco.\n'
                    return False
                # Verifica se o Arquivo ja existe em disco
                elif existeArq:
                    # Se existe retira a operacao da lista de operacoes
                    operacao = self.listaOperacoes.remove(op)
                    print 'Operação {} => Falha'.format(op['idOperacao'])
                    print('O processo {} não pode criar o arquivo {} (Ja existe em disco).\n'.format(processo['PID'], nomeArquivo))
                else:

                    for k, g in groupby(enumerate(self.disco), itemgetter(1)):
                        bloco = map(itemgetter(1), g)
                        if len(bloco) >= numeroBlocos and bloco[0] == -1:
                            execOp = True
                            # Retira a operacao da lista de operacaoes
                            self.listaOperacoes.remove(op)
                            # Insere arquivo na lista de arqArquivos
                            self.listaArquivos.append({'nome': nomeArquivo, 'primeiroBloco': offset, 'quantidadeBlocos': numeroBlocos})
                            fim = offset + numeroBlocos
                            self.disco[offset:fim] = numeroBlocos*[nomeArquivo]
                            print 'Operação {} => Sucesso'.format(op['idOperacao'])
                            print 'O processo {} criou o arquivo {} (blocos {} a {}).\n'.format(processo['PID'], nomeArquivo, offset, fim-1)
                            return True
                        offset = offset + len(bloco)

                    if not execOp:
                        # Manda processo p o fim da fila
                        if op['controlador'] < 1:
                            self.listaOperacoes.append(op)
                            op['controlador'] += 1

                        else:
                            self.listaOperacoes.remove(op)

                        print 'Operação {} => Falha'.format(op['idOperacao'])
                        print('O processo {} não pode criar o arquivo {} (falta de espaço).\n'.format(processo['PID'], nomeArquivo))        #Se é operacao de deletar Arquivo
                        #return False
            ##### OPERACAO PARA DELETAR ARQUIVO ##############
            elif op1:
                op  = op1.pop(0)
                #rem = False
                #verifica se arquivo a ser deletado esta no disco
                arq = [x for x in self.listaArquivos if x['nome'] == op['nomeArquivo']]
                if arq:
                    ini = arq[0]['primeiroBloco']
                    fim = ini + arq[0]['quantidadeBlocos']
                    self.disco[ini:fim] = arq[0]['quantidadeBlocos']*[-1]

                    self.listaArquivos  = [x for x in self.listaArquivos if not x['nome'] == op['nomeArquivo']]
                    self.listaOperacoes.remove(op)
                    print 'Operação {} => Sucesso'.format(op['idOperacao'])
                    print 'O processo {} deletou o arquivo {}.\n'.format(processo['PID'], op['nomeArquivo'])
                else:
                    self.listaOperacoes.remove(op)
                    print 'Operação {} => Falha'.format(op['idOperacao'])
                    print 'O processo {} não pode deletar o arquivo {}. (Nao esta em disco)\n'.format(processo['PID'], op['nomeArquivo'])
            return True
        else:# Se nao houver operacao a ser executada
            #Vai matar o processo e desalocar recursos e memoria
            print 'Nao há mais operação a ser executado pelo processo {}.\n'.format(processo['PID'])
            return False
