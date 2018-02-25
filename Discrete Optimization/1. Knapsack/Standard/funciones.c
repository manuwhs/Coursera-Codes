// Librerias estándar de C
#include <stdio.h>
#include <stdlib.h>

// Librerias de llamadas al sistema de Unix
#include <unistd.h>
#include <fcntl.h>		
#include <sys/types.h>	
#include <sys/stat.h>	

/* Le das el puntero a char * IN y te devuelve el caracter hexadecimal correspondiente a 
ese char y al siguiente */


// void decyp (char* key, char* cad) {
	



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


int copy_vector_char(char * duplicado, char * original, int num) {
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

// Crear arrays de 128 para poner las igualdades relativas a cada caso


	/* Por cada byte del archivo codificado, esta representado como 2 chars de texto plano 'n' -> 19
	Por lo que debemos incrementar el contador del byte de la key cada 2 char leidos 
	Asi pues, primero trataremos el archivo para hacer la conversion, por lo que el nuevo
	número de caracteres se reducira a la mitad */

void get_items (char * data, int * capacity, int * items, int ** weights, int ** values) {
	/* A esta funcion le pasamos el puntero al fichero y nos devuelve un puntero a 
	un array de "key_bytes" strings con los bytes codificados con la misma key */

	int fd_pointer;		/* Numero del byte del arvhivo que estamos tratando */
	int exp = 0;		
	char numero[15];
	fd_pointer = 0;
	int  i;
	char aux_char;


/* Leemos primera línea para obtener numero de elementos y capacidad */

	aux_char = data[fd_pointer];
	while(aux_char != 10 ) {	/* Vamos leyendo cada mensaje encriptado separados por salto= '13'+'10'*/
		if (aux_char != ' ') {
			numero[exp] = aux_char;
			exp++;
		}
		else {
			*items = str2dec(numero,exp);
			printf("Items: %i \n", *items);
			exp = 0;
		}
		fd_pointer++;
		aux_char = data[fd_pointer];

	}
	*capacity = str2dec(numero,exp);
	printf("Capacity: %i \n", *capacity);
	exp = 0;
	fd_pointer++;		/* Para saltarnos el salto '10'*/

/* Aquí ya tenemos el número de items y la capacidad, ahora reservamos memoria y
 vamos poniendo los pesos y valores por cada item */

	*weights = (int *) malloc ((*items)*sizeof(int));
	*values = (int *) malloc ((*items)*sizeof(int));
	if ((weights == NULL)||(values == NULL)) {
		printf ("Error al reservar memoria dinamica");
	}

	printf("Memoria reservada \n");
	for (i = 0; i < *items; i++ ) {
		
	aux_char = data[fd_pointer];
	while(aux_char != 10 ) {	/* Vamos leyendo cada mensaje encriptado separados por salto= '13'+'10'*/
		if (aux_char != ' ') {
			numero[exp] = aux_char;
			exp++;
		}
		else {
			(*values)[i] = str2dec(numero,exp);
			exp = 0;
		}
		fd_pointer++;
		aux_char = data[fd_pointer];
	}
	(*weights)[i] = str2dec(numero,exp);
	exp = 0;
	fd_pointer++;		/* Para saltarnos el salto '10'*/
	}
	printf("Objetos recolectados y listos \n");
}


/* ---------------------------------------------------------------------------------------------------*/
/* Le pasamos el nombre del arhivo a leer, el puntero donde queremos que ponga los datos y nos devuelve el numero de datos leidos */

char * obtener_datos(char * archivo) {

	/*Variables fichero */
	struct stat fd_properties;	/* Estructura predefinida en la que guardaremos 
					datos relevantes al archivo por medio de la funcion "fstat()" --> Obtenemos su tamaño */
  	size_t bytes_fichero;	/* Tamaño del fichero con los messages encriptados*/
	ssize_t errores;	/* Para ver si hay errores (-1) y fin de arvhivo (0)*/
	int fd;			/* Descriptor del fifhero */
	char * data;

	fd = open (archivo, O_RDWR ,0644);  /*El 0644 son los permisos dados si se crea el archivo */

	/* Obtenemos el tamaño del archivo a poner en memoria dinamica */
	errores = fstat(fd, &fd_properties);
	if (errores ==-1) {
		perror("Error al obtener datos del arvhivo:");
		exit(1);
	}
	bytes_fichero = fd_properties.st_size;	/*Ya tenemos el tamaño del archivo */

	/*Leemos todo el archivo de golpe en memoria dinamica  */
	data = (char *) malloc (bytes_fichero*sizeof(char));
	if (data == NULL) {
		printf ("Error al reservar memoria dinamica");
	}
	errores = read(fd, data, bytes_fichero); 

	if (errores==-1) {
		perror("Error al abrir el archivo:");
		exit(1);
	}

	printf ("Archivo leido \n");
	printf ("Datos leidos %i\n",errores);

	errores = close(fd);
	if (errores==-1) {
		perror("Error al cerrar el archivo:");
		exit(1);
	}

	printf ("Archivo cerrado \n");
	return data;
}






