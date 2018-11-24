import sys

def main():

    if len(sys.argv) > 2:
        processos = sys.argv[1]
        arquivos = sys.argv[2]
    else:
        print ("Para rodar corretamente o sistema digite: main.py + 'nome do arquivo de processos' + 'nome do arquivo de arquivos'")

if __name__ == '__main__':
    main()
