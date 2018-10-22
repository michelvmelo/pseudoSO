import sys

if len(sys.argv) != 3:
	exit("\nNumero incorreto de argumentos.\n")

arq_processos = open(sys.argv[1], "r")
arq_arquivos = open(sys.argv[2], "r")

lista_processos = [(x.strip()).split(',') for x in arq_processos.readlines()]
lista_arquivos = [(x.strip()).split(',') for x in arq_arquivos.readlines()]

quantidade_blocos = int(lista_arquivos[0][0])
quantidade_segmentos_ocupados = int(lista_arquivos[1][0])

#cria um dicionario, sendo a chave a identificacao do arquivo e o valor uma lista 
#com o numero do bloco inicial e quantidade de blocos ocupados
blocos_ocupados = {}
for x in range(2, quantidade_segmentos_ocupados+2):
	blocos_ocupados[lista_arquivos[x][0]] = {'bloco_inicial': int(lista_arquivos[x][1]), 
											 'quant_blocos': int(lista_arquivos[x][2])}

#cria uma lista de operacoes a serem realizadas
operacoes = []
for x in range(quantidade_segmentos_ocupados+3, len(lista_arquivos)):
	operacoes.append(lista_arquivos[x])

#cria um dicionario para acessar as informacoes dos processos
processos = {}
for x in range(0, len(lista_processos)):
	processos[x] = {'tempo_inicial': int(lista_processos[x][0]),
					'prioridade': int(lista_processos[x][1]),
					'tempo_cpu': int(lista_processos[x][2]),
					'blocos_mem': int(lista_processos[x][3]),
					'impressora': int(lista_processos[x][4]),
					'scanner': int(lista_processos[x][5]),
					'modem': int(lista_processos[x][6]),
					'disco': int(lista_processos[x][7])}
