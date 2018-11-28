# -*- coding: utf-8 -*-
import GerenciadorMemoria
import GerenciadorRecursos
import GerenciadorDisco

class GerenciadorProcessos(object):

    def __init__(self, files):
        self.gerenciador_memoria = GerenciadorMemoria.GerenciadorMemoria()
        self.gerenciador_recursos = GerenciadorRecursos.GerenciadorRecursos()
        self.gerenciador_disco = GerenciadorDisco.GerenciadorDisco(files)
        self.prioridade = [[], [], [], []]
        self.n = [0, 0, 0, 0]
	self.next_pid = 0
        self.processo = None

    def executar_processo(self, processo):
        if not self.gerenciador_recursos.checagem_de_recursos(processo):
            return
        idx = self.gerenciador_memoria.checagem_de_memoria(processo)
        if idx == -1:
            return
        processo['pid'] = self.next_pid
        self.gerenciador_recursos.alocacao_de_recursos(processo)
        self.gerenciador_memoria.allocate_memoria(processo, idx)
        self.next_pid += 1
        processo['start_tempo'] = processo['tempo']
        self.prioridade[processo['priority']].append(processo)
        self.n[processo['priority']] += 1
        print('dispacher ===>')
        print('\tPID: {}'.format(processo['pid']))
        print('\tpriority: {}'.format(processo['priority']))
        print('\toffset: {}'.format(processo['offset']))
        print('\tblocks: {}'.format(processo['blocks']))
        print('\ttime: {}'.format(processo['tempo']))
        print('\tprinters: {}'.format(processo['printer']))
        print('\tscanners: {}'.format(processo['scanner']))
        print('\tmodems: {}'.format(processo['modem']))
        print('\tdrivers: {}\n'.format(processo['disco']))

	print("\nprocess {} ==>\nP{} STARTED".format(processo['pid'], processo['pid']))

    def filas_vazias(self):
        return self.prioridade == [[], [], [], []] and not self.processo

    def atualiza_prioridade(self, tempo):
        for i, queue in enumerate(self.prioridade):
            if i == 0 or i == 1:
                continue
            atualiza = []
            for j, p in enumerate(queue):
                if tempo - p['init'] >= p['tempo'] / 3.0:
                    atualiza.append(j)
            for u in atualiza:
                print(i, u)
                processo = self.prioridade[i][u]
                self.n[i] -= 1
                self.prioridade[i - 1].append(processo)
                self.n[i - 1] += 1
            self.prioridade[i] = [a for i, a in enumerate(self.prioridade[i])
                                if i not in atualiza]

    def proximo_processo(self, tempo):
        self.atualiza_prioridade(tempo)
        possui_prioridade = next((i for i, x in enumerate(self.n) if x), None)
        if possui_prioridade is not None:
            self.processo = self.prioridade[possui_prioridade].pop(0)
            self.n[possui_prioridade] -= 1
        else:
            self.processo = None

    def proximo_passo(self, tempo):
        if self.processo is None:
            self.proximo_processo(tempo)
            if self.processo is None:
                return

        instruction = self.processo['start_tempo'] - self.processo['tempo'] + 1
        print("P"+str(self.processo['pid'])+" instruction "+str(instruction)),
        if self.processo['priority'] == 0:
            self.processo['tempo'] -= 1
            if self.processo['tempo'] == 0:
                self.gerenciador_memoria.apaga_memoria_processo(self.processo)
                self.gerenciador_recursos.apaga_recursos_processo(self.processo)
                self.gerenciador_disco.operate(self.processo)
                self.proximo_processo(tempo)
        else:
            self.processo['tempo'] -= 1
            if self.processo['tempo'] != 0:
                self.prioridade[self.processo['priority']].append(self.processo)
                self.n[self.processo['priority']] += 1
                self.proximo_processo(tempo)
            else:
                self.gerenciador_memoria.apaga_memoria_processo(self.processo)
                self.gerenciador_recursos.apaga_recursos_processo(self.processo)
                self.gerenciador_disco.operate(self.processo)
                self.proximo_processo(tempo)

