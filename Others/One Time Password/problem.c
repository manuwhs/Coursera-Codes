// Librerias estándar de C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Librerias de llamadas al sistema de Unix
#include <unistd.h>
#include <fcntl.h>		
#include <sys/types.h>	
#include <sys/stat.h>		

char ** get_key_bytes (char * data, size_t key_chars, int bytes_fichero, int * contadores);
char char2hex(char * in);
void zero_char (char * array, int length);
void zero_int (int * array, int length);
void inicia_words (char * words, int n);
void result (char * data, int bytes_fichero, int key_chars, char *key);

int main (int argc, char **argv) {


	/* Parámetros */	
	unsigned char * archivo = "problem1.dat";
	unsigned char * encryp = "6c73d5240a948c86981bc294814d";
//				 6c73d5240a948c86981bc2808548
	unsigned char * text1 = "attack at dawn";
	unsigned char * text2 = "attack at dusk";
	int len;
	
	unsigned char key[20];
	int i, j, k, w, y, p, z;		/* Bucles */

	len = 15;
	
	for (i = 0; i < len; i++){
		key[i] = char2hex(encryp +2*i) ^ text1[i] ;
		printf ("%x", key[i] ^ text2[i]);
	}

}

