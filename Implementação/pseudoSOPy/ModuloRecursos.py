import threading

class GerenciadorRecursos:
    def __init__(self):
        self.sata          = [None, None]
        self.modem         = [None]
        self.scanner       = [None]
        self.impressora    = [None, None]
        self.lock          = threading.Lock()

    # Checa se os recursos que o processo necessita estao disponiveis
    def checarRecursos(self, processo):
        impressora     = processo['impressora']
        scanner        = processo['scanner']
        modem          = processo['modem']
        disco          = processo['disco']
        disponibilidade  = True

        if disco > 0 and self.sata[disco-1] is not None:
            disponibilidade = False
        if modem > 0 and self.modem[0] is not None:
            disponibilidade = False
        if scanner > 0 and self.scanner[0] is not None:
            disponibilidade = False
        if impressora > 0 and self.impressora[impressora-1] is not None:
            disponibilidade = False

        return disponibilidade

    def alocarRecurso(self, processo):
        print("alocar recurso construcao...")
