# -*- coding: utf-8 -*-
class GerenciadorMemoria(object):

    def __init__(self):
        self.memoria = 1024 * [0]

    def checagem_de_memoria(self, processo):
        inicia_memoria_real = 0
        posicao_final_memoria = 0
        if processo['priority'] == 0:
            inicia_memoria_real = 0
            posicao_final_memoria = 64
        else:
            inicia_memoria_real = 64
            posicao_final_memoria = 1024
        ponto_de_partida = inicia_memoria_real
        
        while ponto_de_partida < posicao_final_memoria:
            n = 0
            primeiro = ponto_de_partida
            while (ponto_de_partida != posicao_final_memoria and self.memoria[ponto_de_partida] == 0):
                n += 1
                ponto_de_partida += 1
            else:
                if n >= processo['blocks']:
                    return primeiro
            ponto_de_partida += 1
        return -1

    def allocate_memoria(self, processo, idx):
        processo['offset'] = idx
        self.memoria[idx:idx + processo['blocks']] = processo['blocks'] * [1]
        str_out = 'P{} está alocado em {}, ocupando {} blocos\n'
        idx, o, b = processo['pid'], processo['offset'], processo['blocks']
        print(str_out.format(idx, o, b))

    def apaga_memoria_processo(self, processo):
        processo_end = processo['offset'] + processo['blocks']
        self.memoria[processo['offset']:processo_end] = [0] * processo['blocks']

