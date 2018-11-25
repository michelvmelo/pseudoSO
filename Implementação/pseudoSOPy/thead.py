from threading import Thread
from time import sleep

turn = 0
interessados = [False,False]

class Regiao_critica:
    def __init__(self,processo):
        self.processo = processo

    def enter_regiao(self):
        global turn, interessados

        outro = 1 - self.processo
        interessados[self.processo] = True
        turn = self.processo
        if(turn == self.processo and interessados[outro] == False):
            print "processo %d entrou na regiao critica" %self.processo
        while(turn == self.processo and interessados[outro] == True): pass

    def leave_regiao(self):
        interessados[self.processo] = False
        print "processo %d deixou a regiao critica" %self.processo

class Processo(Thread):

    def __init__(self,processo):
        Thread.__init__(self)
        self.processo = processo

    def run(self):
        r = Regiao_critica(self.processo)

        while True:
            r.enter_regiao()
            r.leave_regiao()
            sleep(3)

p0 = Processo(0)
p1 = Processo(1)

p0.start()
p1.start()
