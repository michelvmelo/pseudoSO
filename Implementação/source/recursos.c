
/*modulo responsável pela liberação ou não dos recursos*/

#define RECURSOS_SERVER
#include "../headers/recursos.h"


/*INICIALIZAÇÃO DOS SEMAFOROS*/
void init_semaphoro(){
	sem_init(&modem, 0, 1);			/*Inicia semaforo com uma permição*/
	sem_init(&driver, 0, 2);		/*Inicia semaforo com duas permição*/
	sem_init(&scanner, 0, 1);		/*Inicia semaforo com uma permição*/
	sem_init(&impressora, 0, 2);	/*Inicia semaforo com duas permições*/
}

int controle_recursos(int recurso){

	return 0;
}