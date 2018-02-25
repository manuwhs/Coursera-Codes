// Librerias estándar de C
#include <stdio.h>
#include <stdlib.h>

// Librerias de llamadas al sistema de Unix
#include <unistd.h>
#include <sys/types.h>

char char2hex(char * in);
void zero_char (char * array, int length);

void main (int argc, char **argv) {
	char as[3] = "5a";
	char caca, i;
	char ar[10];
	caca = char2hex(as);
	printf("\n  %c \n",caca);
	printf("\n  %i \n",caca);

	for (i = 0;i<10; i++) {
		printf("%i \n",ar[i]);
	}
	zero_char(ar,10);
	for (i = 0;i<10; i++) {
		printf("%i \n",ar[i]);
	}
}

