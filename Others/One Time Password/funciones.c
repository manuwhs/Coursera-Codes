// Librerias estándar de C
#include <stdio.h>
#include <stdlib.h>

// Librerias de llamadas al sistema de Unix
#include <unistd.h>
#include <sys/types.h>


/* Le das el puntero a char * IN y te devuelve el caracter hexadecimal correspondiente a 
ese char y al siguiente */


// void decyp (char* key, char* cad) {
	

void inicia_words (char * words, int n) {
	int i;
	int position = 0;
	int last = 1;
	words[position] = ' '; position++;
	for (i = 0; i < 26; i++ ) {	// a - z
		words[last + i] ='a'+i;
		position++;
	}
	last = position;
	
	for (i = 0; i < 26; i++ ) {	// a - z
		words[last + i] ='A'+i;
		position++;
	}
	last = position;

	for (i = 0; i < 10; i++ ) {	// a - z
		words[last + i] ='0'+i;
		position++;
	}

	words[position] = ':'; position++;
	words[position] = ','; position++;
	words[position] = '.'; position++;	
	words[position] = 39;  position++;
	words[position] = '(';  position++;
	words[position] = ')'; position++;
	words[position] = '-'; position++;
}

void mover (char * words, int n) {
	int i;
	char aux;
	char fin = words [n-1];
	for (i = 0; i < n-1; i++){
		words [n-1-i] = words[n-2-i];
	}
	words[0] = fin;
}

		
/* ---------------------------------------------------------------------------------------------------*/

char char2hex(char * in) {
	char num_hex = 2;
	char ci,i, result = 0;
	for (i = 0; i < num_hex ; i++ ) {
		ci = *(in + i);
		if ((ci >= '0')&&(ci <= '9')) {
			result += (1 + 15*(1-i))  * (ci - '0');
		}
		else if ((ci >= 'a')&&(ci <= 'f')) {
			result += (1 + 15*(1-i)) *(ci -'a'+ 10);
		}
		else {
			printf ("\nError de codigos ASCII %i \n ", ci);
		}
	}
	return result;
}




/* Le pasas un array y su longitud y te lo inicializa a 0 */

/* ---------------------------------------------------------------------------------------------------*/

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

// Crear arrays de 128 para poner las igualdades relativas a cada caso


	/* Por cada byte del archivo codificado, esta representado como 2 chars de texto plano 'n' -> 19
	Por lo que debemos incrementar el contador del byte de la key cada 2 char leidos 
	Asi pues, primero trataremos el archivo para hacer la conversion, por lo que el nuevo
	número de caracteres se reducira a la mitad */

char ** get_key_bytes (char * data, size_t key_chars, int bytes_fichero, int *contadores) {
	/* A esta funcion le pasamos el puntero al fichero y nos devuelve un puntero a 
	un array de "key_bytes" strings con los bytes codificados con la misma key */

	int fd_pointer;		/* Numero del byte del arvhivo que estamos tratando */
	int i,m = 0, j,p1,p2;
	int n = 11;			/* Número de mensajes */
	int l_c;		/* Chars del mensaje encriptado */
	int pos_counter[key_chars];	/* Bytes codificcados de key_byte */

	int cont=0;		
	char ** p_out;
	int inicios[n+1];		/* Posicion de inicio de los diferentes mensajes encriptados dentro del fichero */


	fd_pointer = 0;


	zero_int (pos_counter, key_chars);
	zero_int (inicios, n-1);
printf ("Contadores limpiados \n");
printf ("Cadenas: \n");
	while (fd_pointer <= bytes_fichero -10) {	/* Barremos el archivo para ver cuantos datos de cada tipo tiene 
						y donde empiezan los mensajes */

		inicios[m] = fd_pointer;	/* En este punto siempre estaremos al comiendo de un mensaje encriptado
						asi que guardamos su valor */
		cont = 0; 
		while(data[fd_pointer] != 13 ) {	/* Vamos leyendo cada mensaje encriptado separados por salto= '13'+'10'*/

			contadores[cont]++;	/* Incrementamos el contado de dicho byte de la key */
			if (cont < key_chars - 1) {	
				cont++ ;
			}
			else {
				cont = 0;
			}

			fd_pointer += 2;		/* Nos movemos 2 char del fichero (1 byte real) */
		}
		fd_pointer+=2;		/* Por cada mensaje que leamos,incrementados el contador para saltarnos el salto */
		m++;
	}
	inicios[n] = bytes_fichero;

// Vision de lo recolectado:

for ( i = 0; i < n; i ++ ) {
	p1 = inicios[i];
	p2 = inicios[i+1];
	if (p2 == inicios[n]) {
		p2 = p2-2;
	}
	printf("Mensaje %i. Inicio %i. Fin %i Ini-char %c. Fin-char %c \n",i,p1,p2-2, data[p1],data[p2-3]);
}
printf ("Contadores realizados \n");

/* Creamos arrays dinamicos donde pondremos los bytes de la key */

	p_out = (char **)malloc(key_chars*sizeof(char*));		// En la ultima posicion estan los contadores

	for (i = 0; i < key_chars; i++) {
		p_out[i] = (char *) malloc(contadores[i]*sizeof(char));
		if (p_out[i] == NULL) {
			printf("Error");
		}
		zero_char (p_out[i], contadores[i]);
	}

printf ("Memoria reservada \n");


/* Ponemos los bytes encriptados donde corresponde, ya juntamos cada 2 caracteres leidos y tal */



	for (i = 0; i< n -1 ; i++) {   /* Por cada mensaje encriptado */

		l_c = inicios [i+1] - inicios[i] - 2;	/* Chars del mensaje encriptado */
							/*Exepto el ultimo */
		cont = 0; 
		for (j = 0; j < l_c/2; j++) {   /* Por cada 2 char del mensaje encriptado */
			p_out[cont][pos_counter[cont]] = char2hex (data + inicios[i] + 2*j);
			pos_counter[cont]++;			/* Incrementamos la byte de la key al que referenciamos */
			if (cont < key_chars - 1) {	
				cont++ ;
			}
			else {
				cont = 0;
			}

		}
	}

		// El fin de la ultima cadena es el fin del archivo.
		l_c = bytes_fichero - inicios[i] - 4;	/* Chars del mensaje encriptado */
							/*Exepto el ultimo */
		cont = 0; 
		for (j = 0; j < l_c/2; j++) {   /* Por cada 2 char del mensaje encriptado */
			p_out[cont][pos_counter[cont]] = char2hex (data + inicios[i] + 2*j);
			pos_counter[cont]++;			/* Incrementamos la byte de la key al que referenciamos */
			if (cont < key_chars - 1) {	
				cont++ ;
			}
			else {
				cont = 0;
			}

		}


printf("Bytes colocados \n");



/* for (i = 0; i< key_chars; i++) {   
printf("Caracteres key_byte %i: ", i);
	for ( j = 0; j < contadores[i]; j++ ) {
		printf ("%c ", p_out[i][j]);
	}
printf (" \n");
}
*/
	return p_out;
}



/* ---------------------------------------------------------------------------------------------------*/





void result (char * data, int bytes_fichero, int key_chars, char *key) {

	// Obtendremos primero los punteros a los mensajes;

int fd_pointer;		/* Numero del byte del arvhivo que estamos tratando */
	int m = 0, j,i,z;
	int n = 11;			/* Número de mensajes */
	int l_c;		/* Chars del mensaje encriptado */
	char aux;
	char key2[129] = "The secret message is: When using a stream cipher, never use the key more than once";
	int cont=0;		
	int inicios[n-1];		/* Posicion de inicio de los diferentes mensajes encriptados dentro del fichero */

	fd_pointer = 0;

	while (fd_pointer <= bytes_fichero -10) {	/* Barremos el archivo para ver cuantos datos de cada tipo tiene 
						y donde empiezan los mensajes */

		inicios[m] = fd_pointer;	/* En este punto siempre estaremos al comiendo de un mensaje encriptado

						asi que guardamos su valor */
		cont = 0; 
		while(data[fd_pointer] != 13 ) {	/* Vamos leyendo cada mensaje encriptado separados por salto= '13'+'10'*/

			if (cont < key_chars - 1) {	
				cont++ ;
			}
			else {
				cont = 0;
			}

			fd_pointer += 2;		/* Nos movemos 2 char del fichero (1 byte real) */
		}
		fd_pointer+=2;		/* Por cada mensaje que leamos,incrementados el contador para saltarnos el salto */
		m++;
	}

/*	for ( z = 0; z < 83; z++) {
		key [z] = key2[z] ^ char2hex (data + inicios[10] + 2*z) ;
	}
*/

	for (i = 0; i< n -1 ; i++) {   /* Por cada mensaje encriptado */
printf("La cadena es: \n");
		l_c = inicios [i+1] - inicios[i] - 2;	/* Chars del mensaje encriptado */
							/*Exepto el ultimo */
		cont = 0; 
		for (j = 0; j < l_c/2; j++) {   /* Por cada 2 char del mensaje encriptado */
			aux = char2hex (data + inicios[i] + 2*j) ^ key[cont];
			printf("%c", aux);
			if (cont < key_chars - 1) {	
				cont++ ;
			}
			else {
				cont = 0;
			}

		}
printf("\n");	
	}

printf("\n La cadena es: \n");
		// El fin de la ultima cadena es el fin del archivo.
		l_c = bytes_fichero - inicios[10] - 4;	/* Chars del mensaje encriptado */
							/*Exepto el ultimo */
		cont = 0; 
		for (j = 0; j < l_c/2; j++) {   /* Por cada 2 char del mensaje encriptado */
			aux = char2hex (data + inicios[10] + 2*j) ^ key[cont];
			printf("%c", aux);
			if (cont < key_chars - 1) {	
				cont++ ;
			}
			else {
				cont = 0;
			}

		}
printf("\n \n");		
}


