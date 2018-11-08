#include <stdio.h>
#include "../headers/escalonador.h"

int main(int argc, char *argv[]){
	/*char *process_input;	Aponta para arquivo contendo informações do processo*/
	/*char *instruc_input;	Aponta para arquivo contendo informações detalhada do "sistema"*/

	char *process_input;
	if(argc < 2){
		printf("Qtd de arg. invalido.\n");
		printf("Entre com: ./dispacher <processes.txt> <file.txt>\n");
		return -1;
	}

	process_input = argv[1];
	/*instruc_input = argv[2];*/

	read_input_file(process_input);
	return 0;
}