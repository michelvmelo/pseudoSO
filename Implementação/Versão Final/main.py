#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import GerenciadorDisco
import GerenciadorMemoria
import GerenciadorProcessos
import GerenciadorRecursos

def le_arquivos(arquivoProcessos, arquivoDeArquivos):
    listaProcessos = []
    with open(arquivoProcessos, 'r') as processos:
        for processo in processos.readlines():
            processo = processo.replace('\n', '')
            if processo == '':
                continue
            processo = [int(p) for p in processo.split(',')]
            listaProcessos.append({'pid': 0,
                                  'init': processo[0],
                                  'priority': processo[1],
                                  'tempo': processo[2],
                                  'blocks': processo[3],
                                  'printer': processo[4],
                                  'scanner': processo[5],
                                  'modem': processo[6],
                                  'disco': processo[7]})
    with open(arquivoDeArquivos, 'r') as arquivoDeArquivos:
        dados = arquivoDeArquivos.readlines()
        numeroBlocos = int(dados[0])
        numeroSegmentos = int(dados[1])
        arquivos = []
        operacoes = []
        for linha in dados[2: numeroSegmentos + 2]:
            linha = linha.replace('\n', '')
            linha = linha.split(',')
            arquivos.append({'name': linha[0],
                             'first': linha[1],
                             'blocks': linha[2]})
        for linha in dados[numeroSegmentos + 2:]:
            linha = linha.replace('\n', '')
            if linha == '':
                continue
            linha = linha.split(',')
            if len(linha) == 3:
                linha.append('0')
            operacoes.append({'id': linha[0],
                               'code': linha[1],
                               'name': linha[2],
                               'blocks': linha[3]})
        files = {'numeroBlocos': numeroBlocos,
                 'arquivos': arquivos,
                 'operacoes': operacoes}
    return sorted(listaProcessos, key=lambda p: p['init']), files

if __name__ == '__main__':
	
    arquivoProcessos, arquivoDeArquivos = 'processes.txt', 'files.txt'
    if len(sys.argv) == 3:
        arquivoProcessos = sys.argv[1]
        arquivoDeArquivos = sys.argv[2]
    tempo = 0
    processos, files = le_arquivos(arquivoProcessos, arquivoDeArquivos)
    gerenciador_processos = GerenciadorProcessos.GerenciadorProcessos(files)
    while (len(processos) != 0) or (not gerenciador_processos.filas_vazias()):
        if len(processos) != 0:
            while processos[0]['init'] == tempo:
                gerenciador_processos.executar_processo(processos.pop(0))
                if len(processos) == 0:
                    break
        gerenciador_processos.proximo_passo(tempo)
        tempo += 1
        print('')
    disco = gerenciador_processos.gerenciador_disco.disco
    for i, d in enumerate(disco):
        if d == 0:
            disco[i] = (0, 0)
    disco = [str(d[1]) for d in disco]
    print('Organização final do disco:\n')
    print(' | '.join(disco))
    print('')