#ifndef RECURSOS
#define RECURSOS

	#include <stdio.h>
	#include <stdlib.h>
	#include <string.h>
	/*#include "pthread.h"*/
	#include "unistd.h"
	#include <semaphore.h>
	#include <stdbool.h>
	#include <stdint.h>
	
	#ifdef RECURSOS_SERVER
		#define EXT_RECURSOS
	#else
		#define EXT_RECURSOS extern
	#endif

	#define MODEM		1
	#define DRIVER		2
	#define SCANNER		3
	#define IMPRESSORA	4
		
	sem_t impressora;
	sem_t modem;
	sem_t scanner;
	sem_t driver;

	EXT_RECURSOS void init_semaphoro();
	EXT_RECURSOS int controle_recursos(int recurso);
#endif
