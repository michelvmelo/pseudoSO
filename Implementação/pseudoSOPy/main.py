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
	gerenArquivos.numeroBlocos	= int(infoSisArq[0][0])
	gerenArquivos.numeroSegmentos = int(infoSisArq[1][0])
	gerenArquivos.listaArquivos   = [ma.Arquivo(infoSisArq[x]).__dict__ for x in range(2, gerenArquivos.numeroSegmentos + 2)]
	gerenArquivos.listaOperacoes  = [ma.Operacao(infoSisArq[x]).__dict__ for x in range(gerenArquivos.numeroSegmentos + 2, len(infoSisArq))]
	#print(gerenArquivos.listaArquivos)
	#print(gerenArquivos.listaOperacoes)

def operacao(n, sema):
	sema.acquire()
	print("Operacao", n)

def main():
	if len(sys.argv) > 2:
		# Lembrar de verificar a estrutura dos arquivos ???????
		arqProcessos	= open(sys.argv[1], "r")
		arqArquivos	 = open(sys.argv[2], "r")

		listaProcessos  = lerArqProcessos(arqProcessos)
		#print "AQUI!!",listaProcessos
		listaArquivos   = lerArqSistemaArquivos(arqArquivos)
		#print listaArquivos

		gerenArquivos.inicializarDisco()
		
		#tempo = 0
		#while (1):
			#while (gerenArquivos.filaProcessosProntos):
				#if(gerenArquivos.filaProcessosProntos[0]['tempo_inicial') == tempo)
		gerenArquivos.criarArquivo("x", 1, 1)
		#gerenArquivos.opera_processo(gerenProcessos.executando)
		
		####TESTE INICIO#######
		proc = gerenProcessos.filaProcessosProntos.pop(0)
		gerenProcessos.separarProcesso(proc)
		gerenProcessos.executarProcesso(gerenRecursos, gerenMemoria)

		proc = gerenProcessos.filaProcessosProntos.pop(0)
		gerenProcessos.separarProcesso(proc)
		gerenProcessos.executarProcesso(gerenRecursos, gerenMemoria)
		####TESTE FIM#######

		tempoAtual = 0
		# cria threads que representam os processos e as deixa travadas
		# aguardando a liberacao de um release()

		"""
		#laco de tempo, cada volta representa um segundo
		while(len(gerenProcessos.filaProcessosProntos) != 0 ):
			#Separa os processos por prioridade no tempo atual
			while (len(gerenProcessos.filaProcessosProntos) != 0 and gerenProcessos.filaProcessosProntos[0]['tempo_inicial'] <= tempoAtual):
				proc = gerenProcessos.filaProcessosProntos.pop(0)
				gerenProcessos.separarProcesso(proc)

			gerenProcessos.executarProcesso(gerenRecursos, gerenMemoria)
			#gerenProcessos.executarProcesso(gerenRecursos, gerenMemoria)
			tempoAtual += 1 # avanca um segundo no tempo
			print("tempo:", tempoAtual)
			#print("tempo real:", gerenProcessos.filaTempoReal)
			#print("Prioridade 1:", gerenProcessos.prioridade_1)
			#print("Prioridade 2:", gerenProcessos.prioridade_2)
			#print("Prioridade 3:", gerenProcessos.prioridade_3)
		"""

	else:
		print ("Para rodar corretamente o sistema digite: main.py + 'nome do arquivo de processos' + 'nome do arquivo de arquivos'")

if __name__ == '__main__':
	main()
