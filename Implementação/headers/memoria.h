#include <stdio.h>


#ifndef MEMORIA
	#define MEMORIA

	#ifdef MEMORIA_SERVER
		#define EXT_MEMORIA
	#else
		#define EXT_MEMORIA extern
	#endif

	/*typedef struct{
		cFile *tabela_classe;
		int count_class;
	}method_area;
	method_area methodArea;*/

	/*EXT_MEMORIA void init_semaphoro();*/
	/*EXT_ESCALONADOR */
#endif