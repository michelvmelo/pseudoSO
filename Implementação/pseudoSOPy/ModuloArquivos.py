# -*- coding: utf-8 -*-
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
			self.numeroBlocaos = int(info[3])
		else:
			self.numeroBlocaos = None

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
		self.disco = [0 for i in range(self.numeroBlocos)]
		for arquivos in self.listaArquivos:
			# Preenche os blocos do disco com o nome dos arquivos de entrada correspondente
			self.disco[arquivos['primeiroBloco']:arquivos['primeiroBloco'] + arquivos['quantidadeBlocos']] = arquivos['quantidadeBlocos'] *[arquivos['nome']]
		#print(self.disco)
		
	def criarArquivo(self, nome, quantidadeBlocos, ID):
		offset = None
		disponiveis = 0
		fp = open("LOG.txt", "a+")

		if (next((arq for arq in self.arquivos if arq['nome'] == nome), None) is not None):
			string_to_print = "[-] File already exists. PID = "+str(ID)+", FILE = "+str(nome)+"\n"
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
					fp.write(str(string_to_print))
					print "\nDISCAO\n\n",self.disco
					return
			else:
				disponiveis = 0
		string_to_print = "[-] Not enougth space. PID = "+str(ID)+" FILE = "+str(nome)+"\n"
		fp.write(str(string_to_print))
		print "\nDISCAO\n\n",self.disco
		fp.close()
		
	def deletarArquivo(self, arquivos):
		self.disco[arquivos['primeiroBloco']:arquivos['primeiroBloco'] + arquivos['quantidadeBlocos']] = arquivos['quantidadeBlocos'] *[0]

	def execProcesso(self, processo):
		fp = open("LOG.txt", "a+")
		
		#Localiza as operacoes pertencentes ao processo
		ops = [op for op in self.listaOperacoes if op['PID'] == processo['PID']]
		for op in ops:
			#CODIGO PARA CRIACAO
			if op['opcode'] == 0:
				self.criarArquivo(op['arquivo'], op['tamanho'], processo['PID'])
			#CODIGO PARA DELECAO
			else:
				# Seleciona o arquivo pra ser deletado
				nomeArquivo = next((arq for arq in self.arquivos if arq['nome'] == op['arquivo']), None)

				if nomeArquivo is not None:
				#Avalia permissoes
					if (processo['prioridade'] == 0) or (nomeArquivo['criador'] == None or processo['PID'] == nomeArquivo['criador']):
						self.deletarArquivo(arquivo)
						string_to_print = "[+] O processo "+processo['PID']+" deletou o arquivo "+nomeArquivo['nome']
						fp.write(string_to_print)
					else:
						string_to_print = "[-] Permission error. PID = "+processo['PID']+", FILE = "+nomeArquivo['nome']
						fp.write(string_to_print)
				else:
					string_to_print = "[-] File not found. PID = "+processo['PID']+", FILE =  "+op['arquivo']
					fp.write(string_to_print)
			self.operacoes.remove(op)
		fp.close()
