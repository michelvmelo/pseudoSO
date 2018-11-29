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
    gerenProcessos.filaProcessosProntos = sorted(processos, key = itemgetter('tempo_inicial'))
    #print(gerenProcessos.filaProcessosProntos)

# Le o arquivo do sistema de arquivos
def lerArqSistemaArquivos(arquivo):
    infoSisArq = [(x.strip()).replace(' ', '').split(',') for x in arquivo.readlines()]
    listaArquivos = [i for i in infoSisArq]
    gerenArquivos.numeroBlocos    = int(infoSisArq[0][0])
    gerenArquivos.numeroSegmentos = int(infoSisArq[1][0])
    gerenArquivos.listaArquivos   = [ma.Arquivo(infoSisArq[x]).__dict__ for x in range(2, gerenArquivos.numeroSegmentos + 2)]
    operacoes                     = [ma.Operacao(infoSisArq[x]).__dict__ for x in range(gerenArquivos.numeroSegmentos + 2, len(infoSisArq))]
    gerenArquivos.listaOperacoes  = sorted(operacoes, key = itemgetter('idProcesso'))
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
        #for n in range(20):
        while (len(gerenProcessos.filaProcessosProntos) > 0):
            print 'TEMPO: {}'.format(tempo)

            if gerenProcessos.executando:
                aux = gerenArquivos.executaOperacao(gerenProcessos, gerenProcessos.executando)
                if not aux:
                    gerenProcessos.matarprocesso(gerenRecursos, gerenMemoria, gerenProcessos.executando)
                    gerenProcessos.escalonarProcesso(gerenRecursos, gerenMemoria, gerenArquivos)

            else:
                #print gerenProcessos.filaProcessosProntos
                prs = [pr for pr in gerenProcessos.filaProcessosProntos if pr['tempo_inicial'] <= tempo]
                if len(prs) > 0:
                    gerenProcessos.filaProcessosProntos.remove(prs[0])
                    gerenProcessos.separarProcesso(prs[0])
                    gerenProcessos.escalonarProcesso(gerenRecursos, gerenMemoria, gerenArquivos)

            tempo += 1
        gerenArquivos.imprimirDisco()
    else:
        print ("Para rodar corretamente o sistema digite: main.py + 'nome do arquivo de processos' + 'nome do arquivo de arquivos'")

if __name__ == '__main__':
    main()
