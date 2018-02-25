// Librerias estándar de C
#include <stdio.h>
#include <stdlib.h>

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

	/*Variables fichero */
	struct stat fd_properties;	/* Estructura predefinida en la que guardaremos 
					datos relevantes al archivo por medio de la funcion "fstat()" --> Obtenemos su tamaño */
  	size_t bytes_fichero;	/* Tamaño del fichero con los messages encriptados*/
	ssize_t errores;	/* Para ver si hay errores (-1) y fin de arvhivo (0)*/
	int fd;			/* Descriptor del fifhero */

	/* Parámetros */	
	size_t key_bits = 1024;		/* Número de bits de la clave */
	size_t key_chars = key_bits/8;	/* Número de bytes de la clave */
	int n_words = 55;			/* Numero de palabras a comprobar */
	char * archivo = "Datos.dat";

	/* Contadores */
	int i, j, k, w, y, p, z;		/* Bucles */
	int num_encyp_bytes[key_chars];	/* Contiene cuantos bytes encriptados de cada byte de la key tenemos */
	int match_mjw;			/* Elegido un byte 'i' y una letra 'w', esto cuenta el numero de veces que
					 la palabra 'w' puede ser el m1 (cuando m2 sea una letra valida) */
	int num_k;			/* Contados para colocar ordendamente los posibles k's en el array posible_k */

	/* Flags */
	char primera_k;			/* Flag para que solo guardemos las posibles k's una vez y luego reduzcamos.*/

	/* Arrays */
	char * encry_data;		/* Puntero que apunta a todo el archivo de datos encriptados */
	char ** key_byte;	/* Array de punteros que apunta a los bytes encriptados con mismo byte de Key */
	char words [n_words]; /* < a - z > , < A - Z >, ' '    Palabras a utilizar */

	char matches[sizeof(words)/sizeof(char)+1]; /* Posibles valores del mensaje mi (para obtener k hacemos mi xor k xor mi)
						  En la primera posicion pondremos el numero de palabras que coinciden
						 Si es 1 hemos acabado y sino pues nos jodemos */
	char posible_k[sizeof(words)/sizeof(char)+1];	/* Posibles valores de k */ 
	char coincidencias[sizeof(words)/sizeof(char)+1]; /* Coincidencias entre los posibles valores de k dados */

	/* Auxiliares */
	char mj;		/* Es la xor entre 2 bytes encriptados con la misma key_byte y la posible palabra a testear w
				 Si se da que w = m1, entonces el valor de mj sera el m2 del resto */
	char aux;		/* Posible valor de k */
	int length_m;
	char key[key_chars];	/* Palabra código */

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  	zero_int (num_encyp_bytes, key_chars);
	zero_char (key, key_chars);
	inicia_words (words, n_words);


	fd = open (archivo, O_RDWR ,0644);  /*El 0644 son los permisos dados si se crea el archivo */

	/* Obtenemos el tamaño del archivo a poner en memoria dinamica */
	errores = fstat(fd, &fd_properties);
	if (errores ==-1) {
		perror("Error al obtener datos del arvhivo:");
		exit(1);
	}
	bytes_fichero = fd_properties.st_size;	/*Ya tenemos el tamaño del archivo */

	/*Leemos todo el archivo de golpe en memoria dinamica  */
	encry_data = (char *) malloc (bytes_fichero*sizeof(char));
	errores = read(fd, encry_data, bytes_fichero); 

	errores = close(fd);
	if (errores==-1) {
		perror("Error al cerrar el archivo:");
		exit(1);
	}


printf ("Archivo leido \n");
printf ("Datos leidos %i\n",errores);
for (i = 275; i < 283; i++ ){
	printf("%i ", encry_data[i]);
	printf("%c ", encry_data[i]);
	}
printf ("\nDatos leidos %i\n",errores);


	/* Obtenemos el array de 128 strings con los bytes encriptados con el mismo byte de la key 
	Pondra en key_byte los 128 string de byes codificados con el mismo byte de la key
	y en contadores, el numero de bytes de cada uno de los 128*/
printf ("Obtenemos el fichero \n");



	key_byte = get_key_bytes(encry_data, key_chars, (int)bytes_fichero, num_encyp_bytes);



	// OBTENEMOS CLAVE //

for (i=0; i<n_words; i++){
	printf (" %c ", words [i]);
}
printf("\n");

//for ( i = 0; i < key_chars; i++){
//	printf("%i ",num_encyp_bytes[i]);
//}

	for (i = 0; i < key_chars ;i++ )	{	// For every byte in the key 'i'+
		length_m = num_encyp_bytes[i];	/* Numero de bytes codificados con el byte 'i' de la key */
		primera_k = 1;			/* Inicializamos parametros a reusar cada byte_char */
		num_k = 1;
		zero_char (posible_k,sizeof(words)/sizeof(char)+1);
		
// printf ("\n Key_word %i ", i );
		for (j = 0; j<length_m; j++) {		// For every encripter char with the same Key char 'j'
						/* Inicializamos parametros a reusar cada byte encryptado con mismo key_byte  */
			zero_char (matches,sizeof(words)/sizeof(char)+1);
// printf (" \n Position %i \n", j );
			for (w = 0; w < n_words; w++)	{	// For every posible word to try in the key 'w'
				match_mjw = 0;	/* Inicializamos parametros a reusar con cada barrido de 'j' y 'w'  */
				for (k = 0; k < length_m;k++) {		// We make XOR with the rest of them 'k'

					mj = (key_byte[i][j] ^ key_byte[i][k]) ^ words [w];
					if ( (mj >= 'a' && mj <= 'z') || (mj >= 'A' && mj <= 'Z') || (mj==' ')|| (mj=='.')|| (mj==':') ) {
					
						match_mjw ++;
					}
				}
				/* Ya hemos hecho todas las XOR para el byte codificado 'i' con el resto de mensajes para una letra
				Vemos si el byte mi puede corresponder a la letra w y de hacerlo lo indicamos en la tabla */
				if (match_mjw >= num_encyp_bytes[i]){                     /* XXXX */
					matches[0]++ ;	/* Incrementamos el numero de posibles valores de mj */
					matches[w+1] = 1;	/* Indicamos que es un posible valor */
				}
			}
	
if (matches[0]== 1) {			// Si tenemos eso
	for (z = 0; z < n_words; z++){
		if (matches[z+1] == 1) {
			key[i] = words[z] ^ key_byte[i][j];
		}
}


	printf ("Error Key %i, byte %i \n",i,j);
}


/////////////////////////////////////////////////////////////////////////////////////////


/* if ( posible_k[0] <= 1 ) { 
 printf (" \n Fin \n");
break; }
*/

			
		}
	}
	

	printf("La calve es: \n");
	for (i = 0; i < key_chars; i++) {
		printf("  %i ",key[i]);
	}



//	result (encry_data, (int) bytes_fichero, key_chars, key);

	/* Liberamos memoria */
	for (i = 0; i < key_chars; i++) {
		free(key_byte[i]);
	}
	free (key_byte);
	free (encry_data);

	return 0;
}

