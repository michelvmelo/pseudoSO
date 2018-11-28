# -*- coding: utf-8 -*-
from itertools import groupby
from operator import itemgetter

class Arquivo:
    def __init__(self, arquivo, ID = None):
        self.nome = arquivo[0]
        self.primeiroBloco = int(arquivo[1])
        self.quantidadeBlocos = int(arquivo[2])
        self.ID = ID

class Operacao:
    def __init__(self, info):
        self.idProcesso = int(info[0])
        self.codOperacao = int(info[1])
        self.nomeArquivo = info[2]
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

    ''' Inicializa o disco com as informacos de entrada'''
    def inicializarDisco(self):
        # criando um disco com a quantidade de blocos fornecidos na entrada
        self.disco = [-1 for i in range(self.numeroBlocos)]
        for arquivos in self.listaArquivos:
            # Preenche os blocos do disco com o nome dos arquivos de entrada correspondente
            self.disco[arquivos['primeiroBloco']:arquivos['primeiroBloco'] + arquivos['quantidadeBlocos']] = arquivos['quantidadeBlocos'] *[arquivos['nome']]
        #print(self.disco)

    def criarArquivo(self, nome, quantidadeBlocos, ID):
        offset = None
        disponiveis = 0
        fp = open("LOG.txt", "a+")

        if (next((arq for arq in self.arquivos if arq['nome'] == nome), None) is not None):
            string_to_print = "[-] Arquivo ja existe. PID = "+str(ID)+", FILE = "+str(nome)+"\n"
            print(string_to_print)
            fp.write(string_to_print)
            fp.close()
            return

        #localiza espaco disponivel com First Fit e armazena
        for i in range(self.numeroBlocos):
            bloco = self.disco[i]
            if(bloco == 0):
                disponiveis += 1
                if(disponiveis == quantidadeBlocos):
                    offset = i - disponiveis + 1
                    self.disco[offset:offset+disponiveis] = quantidadeBlocos * [nome]
                    arquivo = Arquivo([nome, offset, quantidadeBlocos])
                    self.arquivos.append(arquivo.__dict__)
                    string_to_print = "[+] O processo "+str(ID)+" criou o arquivo "+str(nome)+" (blocos "+str(range(offset,offset+disponiveis))+")\n"
                    print(string_to_print)
                    fp.write(str(string_to_print))
                    #print "\nDISCAO\n\n",self.disco
                    return
            else:
                disponiveis = 0
        string_to_print = "[-] Nao ha espaco em disco. PID = "+str(ID)+" FILE = "+str(nome)+"\n"
        print(string_to_print)
        fp.write(str(string_to_print))
        #print "\nDISCAO\n\n",self.disco
        fp.close()

    def deletarArquivo(self, arquivos):
        self.disco[arquivos['primeiroBloco']:arquivos['primeiroBloco'] + arquivos['quantidadeBlocos']] = arquivos['quantidadeBlocos'] *[-1]

    def executaOperacao(self, processo):
        #fp = open("LOG.txt", "a+")
        PID     = processo['PID']
        print('process {} =>'.format(processo['PID']))
        print('P{} STARTED'.format(processo['PID']))

        #Localiza as operacoes pertencentes ao processo

        #####LEMBRAR QUE EXECUTA UMA OP POR VEZ PARA CADA CICLO #######
        # Se é opercao de criar arquivo
        ops = [op for op in self.listaOperacoes if (op['idProcesso'] == processo['PID'] and op['codOperacao'] == 0)]
        print(ops)
        if ops:
            offset = 0
            execOp = False
            op = ops.pop(0)
            for k, g in groupby(enumerate(self.disco), itemgetter(1)):
                #print(map(itemgetter(1), g))
                bloco = map(itemgetter(1), g)
                if len(bloco) >= op['numeroBlocos'] and bloco[0] == -1:
                    execOp = True
                    # Retira a operacao da lista de operacaoes
                    operacao = self.listaOperacoes.remove(op)

                    fim = offset + op['numeroBlocos']
                    self.disco[offset:fim] = op['numeroBlocos']*[op['nomeArquivo']]
                    print('O processo {} criou o arquivo {} (blocos {} a {}).'.format(processo['PID'], op['nomeArquivo'], offset-1, fim-2))

                    ###### RETIRAR######
                    print(self.disco)
                    break
                offset = offset + len(bloco)
            if not execOp:
                print('O processo {} não pode criar o arquivo {} (falta de espaço).'.format(processo['PID'], op['nomeArquivo']))        #Se é operacao de deletar Arquivo
        else:
            print 'Nao há operação a ser executado pelo processo {}'.format(processo['PID'])

        ops = [op for op in self.listaOperacoes if (op['idProcesso'] == processo['PID'] and op['codOperacao'] == 1)]
        print(ops)
        for op in ops:
            # Verifica se é uma operação do tipo criar Arquivo
            if op['codOperacao'] == 0:
                offset = 0
                execOp = False
                for k, g in groupby(enumerate(self.disco), itemgetter(1)):
                    #print(map(itemgetter(1), g))
                    bloco = map(itemgetter(1), g)
                    if len(bloco) >= op['numeroBlocos'] and bloco[0] == -1:
                        execOp = True
                        # Retira a operacao da lista de operacaoes
                        operacao = self.listaOperacoes.pop(0)
                        fim = offset + op['numeroBlocos']
                        self.disco[offset:fim] = op['numeroBlocos']*[operacao['nomeArquivo']]
                        print('O processo {} criou o arquivo {} (blocos {} a {}).'.format(processo['PID'], operacao['nomeArquivo'], offset, fim-1))

                        ###### RETIRAR######
                        print(self.disco)
                        break
                    offset = offset + len(bloco)
                if execOp:
                    print('O processo {} não pode criar o arquivo {} (falta de espaço).'.format(processo['PID'], op['nomeArquivo']))
            else:
                print 'MODIFICAR: O processo ? deletou o arquivo ?.'
                print 'MODIFICAR: O processo ? não pode deletar o arquivo ?.'

        '''
        i = 1
        for op in ops:
            print('P{} instruction {}'.format(processo['PID'], i))
            i += 1
            #CODIGO PARA CRIACAO
            if op['codOperacao'] == 0:
                self.criarArquivo(op['nomeArquivo'], op['numeroBlocos'], processo['PID'])
            #CODIGO PARA DELECAO
            else:
                # Seleciona o arquivo pra ser deletado
                nomeArquivo = next((arq for arq in self.arquivos if arq['nome'] == op['arquivo']), None)

                if nomeArquivo is not None:
                #Avalia permissoes
                    if (processo['prioridade'] == 0) or (nomeArquivo['criador'] == None or processo['PID'] == nomeArquivo['criador']):
                        self.deletarArquivo(arquivo)
                        string_to_print = "[+] O processo "+processo['PID']+" deletou o arquivo "+nomeArquivo['nome']
                        print(string_to_print)
                        fp.write(string_to_print)
                    else:
                        string_to_print = "[-] Permission error. PID = "+processo['PID']+", FILE = "+nomeArquivo['nome']
                        print(string_to_print)
                        fp.write(string_to_print)
                else:
                    string_to_print = "[-] File not found. PID = "+processo['PID']+", FILE =  "+op['arquivo']
                    print(string_to_print)
                    fp.write(string_to_print)
            self.listaOperacoes.remove(op)
        '''
        #fp.close()
