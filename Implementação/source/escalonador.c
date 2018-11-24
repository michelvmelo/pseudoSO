#include <stdio.h>
#include "../headers/escalonador.h"

void read_input_file(char *input_file){

	FILE *read_input;
	char str[10];
	char *colum_Str, c;

	memset(str, '\0', 10);

	read_input = fopen(input_file, "r");

	if(read_input == NULL){
		printf("Não foi possivel abrir o arquivo de processos.\n");
	}else{
		while((fscanf (read_input, "%[^\n]", str)) != EOF){

			colum_Str = strtok(str, ",");
			if(colum_Str != NULL)
				printf("%s ", colum_Str);

			c = getc(read_input);

			while(colum_Str != NULL){
				colum_Str = strtok(NULL, ",");
				if(colum_Str != NULL)
					printf("%s ", colum_Str);
			}
			printf("\n");
		}
	}
}