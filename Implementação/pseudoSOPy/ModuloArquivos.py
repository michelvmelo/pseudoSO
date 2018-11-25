class Arquivo:
    def __init__(self, arquivo):
        self.nome = arquivo[0]
        self.primeiroBloco = int(arquivo[1])
        self.quantidadeBlocos = int(arquivo[2])

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

    ''' Inicializa o disco com as informacos de entrada'''
    def inicializarDisco(self):
        # criando um disco com a quantidade de blocos fornecidos na entrada
        self.disco = [0 for i in range(self.numeroBlocos)]
        for arquivos in self.listaArquivos:
            # Preenche os blocos do disco com o nome dos arquivos de entrada correspondente
            self.disco[arquivos['primeiroBloco']:arquivos['primeiroBloco'] + arquivos['quantidadeBlocos']] = arquivos['quantidadeBlocos'] *[arquivos['nome']]
        #print(self.disco)
