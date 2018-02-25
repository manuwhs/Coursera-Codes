// Librerias estándar de C
#include <stdio.h>
#include <stdlib.h>

// Librerias de llamadas al sistema de Unix
#include <unistd.h>
#include <fcntl.h>		
#include <sys/types.h>	
#include <sys/stat.h>	
#include "funciones.h"

/* Le das el puntero a char * IN y te devuelve el caracter hexadecimal correspondiente a 
ese char y al siguiente */

	



/* Le pasas un array y su longitud y te lo inicializa a 0 */


void zero_char (char * array, int length) {
	int i ;
	for (i = 0; i < length; i++) {
		*(array + i) = 0;
	}
}

/* ---------------------------------------------------------------------------------------------------*/

void zero_int (int * array, int length) {
	int i ;
	for (i = 0; i < length; i++) {
		*(array + i) = 0;
	}
}

/* ---------------------------------------------------------------------------------------------------*/

int str2dec(char  * cad, char digit) {
	int out = 0;
	int i, j;
	int aux;
	
	for (i = 0; i < digit; i++) { 
		aux = cad[i] - '0';
		if((digit -i ) > 0 ) {
			for (j = 1; j < digit - i; j++) {
				aux = aux * 10;
			}
		}
		out += aux;
	}
	return out;
}

/* ---------------------------------------------------------------------------------------------------*/

float str2float(char  * cad, char digit) {
	float out = 0;
	int i, j;
	float aux;
	
	i = 0;
	
	while (cad[i] != '.') {
		aux = cad[i] - '0';
		if((digit -i ) > 0 ) {
			for (j = 1; j < digit - i; j++) {
				aux = aux * 10;
			}
		}
		out += aux;
		i++;
	}
	i++;
	for (i = i; i < digit; i++) { 
		aux = cad[i] - '0';
		if((digit -i ) > 0 ) {
			for (j = i; j < digit - i; j++) {
				aux = aux / 10;
			}
		}
		out += aux;
	}

	return out;
}

/* ---------------------------------------------------------------------------------------------------*/
/* Ordena de mayor a menor un array de int */
int ordenar_int (int * lista, int * orden, int len) {
 
	int aux_big; 
	int aux_pos, aux; 
	int i,j;
	
	for (i = 0; i < len ; i++) {
		orden[i] = i;
	}

	for(i = 0 ;i < len - 1; i++) {
		aux_big = lista[i];
		aux_pos = i;

		for (j = i + 1; j < len; j++) {

			if(aux_big < lista[j]) {
				aux_big = lista [j];
				aux_pos = j;
			}
		 }
		lista[aux_pos] = lista[i];
		lista[i] = aux_big;

		aux = orden[aux_pos];
		orden[aux_pos] = orden[i];
		orden[i] = aux;
	 }
	return 1;
}
/* ---------------------------------------------------------------------------------------------------*/
/* Reordena un array tal y como le indica otro */
int reordenar_int (int * lista, int * orden, int len) {
 	int nueva_lista [len];
	int i;
	for(i = 0 ;i < len ; i++) {
		nueva_lista[i] = lista[orden[i]];
	 }
	 copy_vector_int(lista, nueva_lista, len);
	return 1;
}
/* ---------------------------------------------------------------------------------------------------*/
int desreordenar_char (char * lista, int * orden, int len) {
 	char nueva_lista [len];
	int i;
	for(i = 0 ;i < len ; i++) {
		nueva_lista[orden[i]] = lista[i];
	 }
	 copy_vector_char(lista, nueva_lista, len);
	return 1;
}

/* ---------------------------------------------------------------------------------------------------*/




int dec2str(char  * cad, int digit) {
	int i, j;
	int aux;
	
	i = 0;
	aux = digit;
	while (aux != 0 ) {
		cad[i] = aux % 10 + '0';
		aux = aux / 10;
		i++;
	}
	cad[i] = '\0';
	
	printf("%s \n", cad);
	for (j = 0; j < i/2; j++){
		aux = cad[j];
		cad[j] = cad[i - 1 -j];
		cad[i - 1 -j] = aux;
	}
	printf("%s \n", cad);
	return 1;
}

/* ---------------------------------------------------------------------------------------------------*/


int max(int a, int b) { 
	return (a > b)? a : b;
}


/* ---------------------------------------------------------------------------------------------------*/

float maxf (float * array, int num) {
	int i;
	float aux = array[0];

	for (i = 1; i < num; i++) {
		if (array[i] > aux) {
			aux = array[i];
		}
	}
	return aux;
}

/* ---------------------------------------------------------------------------------------------------*/





int findint(int * array, int len, int value) {
	int i;
	for (i = 0; i < len ; i++ ) {
		if (array[i] == value ) {
//			printf("Found on position: %i\n", i);
			return i;
		}
	}
	return -1;  /* Not found */
}

/* ---------------------------------------------------------------------------------------------------*/

int copy_vector_char(char * duplicado, char * original, int num) {
	int i;
	for (i = 0; i < num; i++) {
		duplicado[i] = original[i];
	}
	return 1;
}

/* ---------------------------------------------------------------------------------------------------*/

int copy_vector_int(int * duplicado, int * original, int num) {
	int i;
	for (i = 0; i < num; i++) {
		duplicado[i] = original[i];
	}
	return 1;
}

/* ---------------------------------------------------------------------------------------------------*/


int count_char(char * array, int len, int value) {
	int i;
	int count = 0;
	for (i = 0; i < len ; i++ ) {
		if (array[i] == value ) {
//			printf("Found on position: %i\n", i);
			count++;
		}
	}
	return count;  /* Not found */
}

/* ---------------------------------------------------------------------------------------------------*/


