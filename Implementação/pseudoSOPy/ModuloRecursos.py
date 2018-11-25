import threading

class GerenciadorRecursos:
    def __init__(self):
        self.sata1         = None
        self.sata2         = None
        self.modem         = None
        self.scanner       = None
        self.impressora1   = None
        self.impressora2   = None

        self.alocarMutex         = threading.Semaphore()
        self.desalocarMutex      = threading.Semaphore()

    # Checa se os recursos que o processo necessita estao disponiveis
    def checarRecursos(self, processo):
        impressora     = processo['impressora']
        scanner        = processo['scanner']
        modem          = processo['modem']
        disco          = processo['disco']
        disponibilidade  = True

        if disco == 1 and self.sata1 is not None:
            disponibilidade = False
        if disco == 2 and self.sata2 is not None:
            disponibilidade = False
        if modem > 0 and self.modem is not None:
            disponibilidade = False
        if scanner > 0 and self.scanner is not None:
            disponibilidade = False
        if impressora == 1 and self.impressora1 is not None:
            disponibilidade = False
        if impressora == 2 and self.impressora2 is not None:
            disponibilidade = False
        return disponibilidade

    def alocarRecurso(self, processo):
        self.alocarMutex.acquire() # Permite que apenas um processo entre nessa regiao por vez
        impressora     = processo['impressora']
        scanner        = processo['scanner']
        modem          = processo['modem']
        disco          = processo['disco']
        PID            = processo['PID']
        # reserva o recurso para o processo
        if disco == 1:
            self.sata1 = PID
        if disco == 2:
            self.sata2 = PID
        if impressora == 1:
            self.modem = PID
        if impressora == 2:
            self.scanner = PID
        if scanner == 1:
            self.impressora1 = PID
        if modem == 1:
            self.impressora1 = PID
        self.alocarMutex.release()

        ####TESTE INICIO#######
        print(  self.sata1,
                self.sata2,
                self.modem ,
                self.scanner,
                self.impressora1,
                self.impressora2 )
        ####TESTE fim#######    
    def desalocarRecurso(self, processo):
        self.desalocarMutex.acquire()
        PID = processo['PID']

        if self.sata1 == PID:
            self.sata1 = None
        if self.sata2 == PID:
            self.sata2 = None
        if self.modem == PID:
            self.modem = None
        if self.scanner  == PID:
            self.scanner = None
        if self.impressora1 == PID:
            self.impressora1 = None
        if self.impressora2 == PID:
            self.impressora2 = None
        self.desalocarMutex.release()
