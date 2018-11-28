class GerenciadorDisco(object):

    def __init__(self, files):
        self.disco = files['numeroBlocos'] * [0]
        self.arquivos = files['arquivos']
        for archive in self.arquivos:
            primeiro = int(archive['first'])
            blocos = int(archive['blocks'])
            nome = archive['name']
            self.disco[primeiro:primeiro + blocos] = blocos * [(0, nome)]
        self.operacoes = files['operacoes']

    def deletar_arquivo_disco(self, processo, nome):
        pid = processo['pid']
        tamanho = 0
        primeiro = -1
        if processo['priority'] != 0:
            for i, d in enumerate(self.disco):
                if d == 0:
                    continue
                if d == (0, nome) or d == (pid, nome):
                    if primeiro == -1:
                        primeiro = i
                    tamanho += 1
                elif primeiro != -1:
                    break
            if primeiro != -1:
                self.disco[primeiro:primeiro + tamanho] = tamanho * [0]
                return True
            else:
                return False
        else:
            for i, d in enumerate(self.disco):
                if d == 0:
                    continue
                if d[1] == nome:
                    if primeiro == -1:
                        primeiro = i
                    tamanho += 1
                elif primeiro != -1:
                    break
            if primeiro != -1:
                self.disco[primeiro:primeiro + tamanho] = tamanho * [0]
                return True
            else:
                return False

    def adiciona_arquivo_disco(self, pid, nome, blocos):
        blocos = int(blocos)
        i = 0
        limite_v = len(self.disco)
        while i < limite_v:
            n = 0
            primeiro = i
            while i != limite_v and self.disco[i] == 0:
                n += 1
                i += 1
            else:
                if n >= blocos:
                    self.disco[primeiro:primeiro + blocos] = blocos * [(pid, nome)]
                    return primeiro, blocos
            i += 1
        return -1, -1

    def operate(self, processo):
	
        i = 0

        for op in self.operacoes:
            if int(op['id']) == processo['pid']:
                i += 1
                if int(op['code']) == 1:
                    if self.deletar_arquivo_disco(processo, op['name']):
                        pid = processo['pid']
                        nome = op['name']
			print("[+] Arquivo "+str(nome)+" deletado com sucesso. OP"+str(i)+"\n")
                    else:
                        pid = processo['pid']
                        nome = op['name']
			print("\n[-] Falha ao deletar o arquivo."+str(nome)+", OP"+str(i)+"\n")
		else:
                    aux = self.adiciona_arquivo_disco(processo['pid'], op['name'], op['blocks'])
                    if aux != (-1, -1):
                        pid = processo['pid']
                        nome = op['name']
                        end = aux[0] + aux[1] - 1
			print("[+] Arquivo "+str(nome)+" adicionado com sucesso. OP"+str(i)+" dos blocos "+str(aux[0])+" ao "+str(end)+".\n")
                    else:
                        pid = processo['pid']
                        nome = op['name']
			print("\n[-] Falha ao deletar o arquivo "+str(nome)+". OP"+str(i)+"\n")
