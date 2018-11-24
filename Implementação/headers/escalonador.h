#include <stdio.h>
#include <string.h>


#ifndef ESCALONADOR
#define ESCALONADOR

	#ifdef ESCALONADOR_SERVER
		#define EXT_ESCALONADOR
	#else
		#define EXT_ESCALONADOR extern
	#endif

	/*typedef struct{
		cFile *tabela_classe;
		int count_class;
	}method_area;
	method_area methodArea;*/

	EXT_ESCALONADOR void read_input_file(char *input_file);
	/*EXT_ESCALONADOR */
#endif