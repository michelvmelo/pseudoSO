#include <stdio.h>


#ifndef PROCESSOS
	#define PROCESSOS

	#ifdef PROCESSOS_SERVER
		#define EXT_PROCESSOS
	#else
		#define EXT_PROCESSOS extern
	#endif

	/*typedef struct{
		cFile *tabela_classe;
		int count_class;
	}method_area;
	method_area methodArea;*/

	/*EXT_PROCESSOS void init_semaphoro();*/
	/*EXT_ESCALONADOR */
#endif