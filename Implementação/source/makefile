all: build clean

build: escalonador.o memoria.o processos.o recursos.o main.o
	@echo "Criando executavel...Pronto!"
	@gcc escalonador.o memoria.o processos.o main.o recursos.o -ansi -std=c99 -lcunit -o dispatcher -Wall -g -lm

main.o: main.c
	@echo "Compilando..."
	@gcc -c -ansi -Wall -std=c99 main.c -lcunit -g

processos.o: processos.c
	@gcc -c -ansi -Wall -std=c99 processos.c -lcunit -g

memoria.o: memoria.c
	@gcc -c -ansi -Wall -std=c99 memoria.c -lcunit -g

recursos.o: recursos.c
	@gcc -c -ansi -Wall -std=c99 recursos.c -lcunit -g

escalonador.o: escalonador.c
	@gcc -c -ansi -Wall -std=c99 escalonador.c -lcunit -g

clean:
	@rm *.o