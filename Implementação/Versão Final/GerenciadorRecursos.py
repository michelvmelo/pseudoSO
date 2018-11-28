class GerenciadorRecursos(object):

    def __init__(self):
        self.recursos = {'scanner': 0, 'printers': [0, 0], 'modem': 0, 'drivers': [0, 0]}

    def checagem_de_recursos(self, processo):
        if processo['scanner'] == 1:
            if self.recursos['scanner'] == 1:
                return False
        if processo['modem'] == 1:
            if self.recursos['modem'] == 1:
                return False
        if processo['printer'] != 0:
            if self.recursos['printers'][processo['printer'] - 1] == 1:
                return False
        if processo['disco'] != 0:
            if self.recursos['drivers'][processo['disco'] - 1] == 1:
                return False
        return True

    def alocacao_de_recursos(self, processo):
	        if processo['scanner'] == 1:
            self.recursos['scanner'] = 1
            print("P"+str(processo['pid'])+" alocou scanner.\n")
        if processo['modem'] == 1:
            self.recursos['modem'] = 1
            print("P"+str(processo['pid'])+" alocou modem.\n")
        if processo['printer'] != 0:
            self.recursos['printers'][processo['printer'] - 1] = 1
	    print("P"+str(processo['pid'])+" alocou impressora "+str(processo['printer'] - 1)+"\n")
        if processo['disco'] != 0:
            self.recursos['drivers'][processo['disco'] - 1] = 1
            sata_str = "\tP{} allocated SATA {}."
	    print("P"+str(processo['pid'])+" alocou SATA "+str(processo['disco']-1)+"\n")
	

    def apaga_recursos_processo(self, processo):
        if processo['scanner'] == 1:
            self.recursos['scanner'] = 0
        if processo['modem'] == 1:
            self.recursos['modem'] = 0
        if processo['printer'] != 0:
            self.recursos['printers'][processo['printer'] - 1] = 0
        if processo['disco'] != 0:
            self.recursos['drivers'][processo['disco'] - 1] = 0

