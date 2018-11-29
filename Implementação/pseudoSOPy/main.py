# -*- coding: utf-8 -*-

import sys
import threading
from operator import itemgetter
import ModuloMemoria   as mm
import ModuloArquivos  as ma
import ModuloProcessos as mp
import ModuloRecursos  as mr

# inicia os modulos de genernciamento do sistema
gerenMemoria   = mm.GerenciadorMemoria()
gerenArquivos  = ma.GerenciadorArquivos()
gerenRecursos  = mr.GerenciadorRecursos()
gerenProcessos = mp.GerenciadorProcessos()

# Le o aqrquivo de processos
def lerArqProcessos(arquivo):
    lista_processos = [(x.strip()).split(',') for x in arquivo.readlines()]
    #cria um dicionario para acessar as informacoes dos processos
    processos = [mp.Processo(proc).__dict__ for proc in lista_processos]
    # insere os precessos na fila de pronto por ordem de tempo de inicializacao
    gerenProcessos.listaProcessos = sorted(processos, key = itemgetter('tempo_inicial'))
    #print(gerenProcessos.filaProcessosProntos)

# Le o arquivo do sistema de arquivos
def lerArqSistemaArquivos(arquivo):
    infoSisArq = [(x.strip()).replace(' ', '').split(',') for x in arquivo.readlines()]
    listaArquivos = [i for i in infoSisArq]
    gerenArquivos.numeroBlocos    = int(infoSisArq[0][0])
    gerenArquivos.numeroSegmentos = int(infoSisArq[1][0])
    gerenArquivos.listaArquivos   = [ma.Arquivo(infoSisArq[x]).__dict__ for x in range(2, gerenArquivos.numeroSegmentos + 2)]
    gerenArquivos.listaOperacoes  = [ma.Operacao(infoSisArq[x]).__dict__ for x in range(gerenArquivos.numeroSegmentos + 2, len(infoSisArq))]
    gerenArquivos.numerarOperacoes()
    #print(gerenArquivos.listaArquivos)
    #print(gerenArquivos.listaOperacoes)
    #print gerenArquivos.numeroSegmentos

def operacao(n, sema):
    sema.acquire()
    print("Operacao", n)

def main():
    process_file, files_file = 'processes.txt', 'files.txt'
    if len(sys.argv) > 2:
        # Lembrar de verificar a estrutura dos arquivos ???????
        arqProcessos    = open(sys.argv[1], "r")
        arqArquivos     = open(sys.argv[2], "r")

        listaProcessos  = lerArqProcessos(arqProcessos)
        listaArquivos   = lerArqSistemaArquivos(arqArquivos)

        gerenArquivos.inicializarDisco()

        tempo = 0
        for n in range(20):
        #while True:

            maiorPrioridade = None

            if len(gerenProcessos.listaProcessos) == 0 and len(gerenProcessos.filaProcessosProntos) == 0 and len(gerenArquivos.listaOperacoes) == 0:
                break

            l  = [pr for pr in gerenProcessos.listaProcessos if pr['tempo_inicial'] == tempo]
            gerenProcessos.filaProcessosProntos = gerenProcessos.filaProcessosProntos + l
            gerenProcessos.listaProcessos = [x for x in gerenProcessos.listaProcessos if x['tempo_inicial'] != tempo]


            # Escalonador de processo
            if len(gerenProcessos.filaProcessosProntos) > 0 or gerenProcessos.executando:
                print 'TEMPO: {}'.format(tempo)
                if len(gerenProcessos.filaProcessosProntos) > 0:
                    #print gerenProcessos.filaProcessosProntos
                    naoExecutados = [x for x in gerenProcessos.filaProcessosProntos if x['PID'] == None]
                    if len(naoExecutados) > 0:
                        maiorPrioridade = min(naoExecutados, key=lambda x:x['prioridade'])
                    else:
                        maiorPrioridade = gerenProcessos.filaProcessosProntos[0]

                    #print maiorPrioridade
                    #gerenProcessos.filaProcessosProntos = [x for x in gerenProcessos.filaProcessosProntos if x != maiorPrioridade]
                    #print gerenProcessos.filaProcessosProntos
                    #print gerenProcessos.filaProcessosProntos

                    if gerenProcessos.executando:
                        #print 1
                        if maiorPrioridade['prioridade'] < gerenProcessos.executando['prioridade']:
                            #print 2
                            if gerenArquivos.verificarOperacoes(gerenProcessos.executando['PID']):
                                #print 3
                                gerenProcessos.filaProcessosProntos.append(gerenProcessos.executando)
                                gerenProcessos.desalocar(gerenRecursos, gerenMemoria, gerenProcessos.executando)
                                gerenProcessos.criarProcesso(gerenRecursos, gerenMemoria, gerenArquivos, maiorPrioridade)
                            else:
                                #print 4
                                if maiorPrioridade['PID']:
                                    #print 5
                                    gerenArquivos.executaOperacao(gerenRecursos, gerenMemoria, gerenProcessos, maiorPrioridade)
                                else:
                                    #print 6
                                    gerenProcessos.criarProcesso(gerenRecursos, gerenMemoria, gerenArquivos, maiorPrioridade)
                        else:
                            print 7
                            if gerenArquivos.verificarOperacoes(gerenProcessos.executando['PID']):
                                #print 8
                                gerenArquivos.executaOperacao(gerenRecursos, gerenMemoria, gerenProcessos, gerenProcessos.executando)
                            else:
                                #print 9
                                gerenProcessos.desalocar(gerenRecursos, gerenMemoria, gerenProcessos.executando)
                                if maiorPrioridade['PID']:
                                    #print 10
                                    gerenArquivos.executaOperacao(gerenRecursos, gerenMemoria, gerenProcessos, maiorPrioridade)
                                else:
                                    #print 11
                                    gerenProcessos.criarProcesso(gerenRecursos, gerenMemoria, gerenArquivos, maiorPrioridade)
                    else:
                        #print 12
                        if maiorPrioridade['PID']:
                            #print 13
                            if gerenArquivos.verificarOperacoes(maiorPrioridade['PID']):
                                #print 14
                                gerenArquivos.executaOperacao(gerenRecursos, gerenMemoria, gerenProcessos, maiorPrioridade)
                            else:
                                #print 16
                                gerenProcessos.desalocar(gerenRecursos, gerenMemoria, maiorPrioridade)
                                gerenProcessos.filaProcessosProntos.remove(maiorPrioridade)
                        else:
                            #print 15
                            gerenProcessos.criarProcesso(gerenRecursos, gerenMemoria, gerenArquivos, maiorPrioridade)
                else:
                    #print 16
                    if gerenArquivos.verificarOperacoes(gerenProcessos.executando['PID']):
                        #print 17
                        gerenArquivos.executaOperacao(gerenRecursos, gerenMemoria, gerenProcessos, gerenProcessos.executando)
                    else:
                        #print 17
                        break

            tempo += 1

            #print gerenArquivos.listaOperacoes
        gerenArquivos.imprimirDisco()
    else:
        print ("Para rodar corretamente o sistema digite: main.py + 'nome do arquivo de processos' + 'nome do arquivo de arquivos'")

if __name__ == '__main__':
    main()
