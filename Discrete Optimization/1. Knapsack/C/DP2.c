
#include "funciones.h"
#include <stdio.h>
#include <stdlib.h>

#include <unistd.h>
#include <fcntl.h>		
#include <sys/types.h>	
#include <sys/stat.h>	
/*------------------------------------------------------------------------------------------------ */


/*------------------------------------------------------------------------------------------------ */
/* Normal Knapsak bottom - up */

/* IDEA:
We are gonna asume we have enough memory to allocate the table (column by column) but columns are too
big and there is no enough "free big spaces" to allocate it so we have to split columns.
We will do the following: 
	We try allocating all the columns in the memory
	If we cannot fit them all, we free all previous allocated memory and break the columns in "N"
	If this still cannot be allocated we break them into smaller pieces 
*/

int  DP(int capacity, int items, int * weights, int * values, int * best, char * taken_out) {
   int i, j, c;
   int ** K;
   int aux;
   int cont= 0;
   char taken[items];
   int row, column; 	/* For trace-back */
   int rest;		/* Rest of the fraction of the columns */
   int cap_per_point;
   int * caps;
   int * starts;

   int aux_rest;
   int extra;
   int pointer, desp;
			/* We will always assing the "more capacities" to the first pointers*/
 
   int N = 1;		/* Fractions of the columns */

/* Reservamos memoria dinámica */
/* Number of columns (pointers per columns) */


   K = (int **) malloc (( N )*(items +1)*sizeof(int *));
	if (K == NULL) {
		printf ("Error al reservar memoria dinamica");
	}

   rest = (capacity + 1) % N;

   cap_per_point = capacity / N;

   cont = 0;

   /* To avoid having to check at every capacity the pointer we should look into, we will create an array with
   the value of the capacity that every pointer has.
   caps = [capacity_pointer_1,capacity_pointer_2,capacity_pointer_3... ] */ 

   /* GETTING CAPS */
   caps = (int *) malloc ( N * sizeof(int ));
   if (caps == NULL) {",i, cont);
	perror(" Error al reservar memoria dinamica");
    }

   for (i = 0; i < N; i++) {
	if (rest > 0 )  {
		extra = 1;
		rest --;
	}
	else {
		extra = 0;
	}
	caps[i] = cap_per_point + extra;
   }

   /* GETTING STARTS */

   starts = (int *) malloc ( N * sizeof(int ));
   if (caps == NULL) {",i, cont);
	perror(" Error al reservar memoria dinamica");
    }

   starts[0] = 0;

   for (i = 0; i < N - 1; i++) {
	starts[i + 1] = starts[i] + caps[i];


   for (i = 0; i < (items + 1); i++){	/* For every column */
	
	 for (j= 0; j < N; j++) {	/* For every pointer per column */

  	 	K[i + j] = (int *) malloc ( caps[i]*sizeof(int ));

		if (K[i + j ] == NULL) {
			cont++;
			printf  ("Error al reservar memoria dinamica para el item %i. Error %i \n",i, cont);
			perror(" Error al reservar memoria dinamica");
			
		}
	 }
   }


   printf("Realizando DP correctament.... \n");


   for (i = 0; i <= items; i++){			/* For every item (column (formed by N pointers)*/
	 for (n = 0; n < N; n++) {			/* For every pointer per column */
       		for (c = starts[n]; c < starts; c++){	/* For every capacity */


           if (i==0 || c==0) {
               K[i][c] = 0;
	   }
           else if (weights[i-1] <= c)
                 K[i][c] = max(values[i-1] + K[i-1][c-weights[i-1]],  K[i-1][c]);
/* e choose the maximum beteen the same value of the last table 
and the value of every object plus the value os the last table ith enought
space left to put that object */
           else
                 K[i][c] = K[i-1][c];
       }
   }



/*
for (c = 0; c <= capacity; c++){
   for (i = 0; i <= items; i++){

		printf("%d \t",K[i][c]);
	}
	printf("\n");
   }
*/

/* We output the best value */

	*best  = K[items][capacity];


/* We start trace-back */

zero_char(taken,items);
aux = K[items][capacity];
column = items;
row = capacity;


/* K [column][row] */
for (i = 0; i < items; i++) {
//	printf("Comparamos: %i - %i \n",K[column][row],K[column -1][row]);
	if (K[column][row] > K[column -1][row]) {	/* Si no son iguales cojemos el objeto */
		taken[column - 1] = 1;
		aux = aux - values[column - 1];
//		printf("value %i  aux %i \n",values[column - 1],aux);
		row = findint(K[column - 1], capacity + 1, aux ); /* Buscamos en la columna anterior */
		column--;
	}
	else {
//		printf("Quitado\n");
		if (K[column][row] == 0){
			break;
		}
		column--;
	}

}

/* Output the taken objects */
copy_vector_char(taken_out, taken, items); 

/*
	for (i = 0; i < items; i++) {
		printf("%i ", taken_out[i]);
	}
	printf("\n\n");
*/
/*
for (i = 0; i < items; i++) {
	printf ("%i ",taken[i]);
	}
	printf("\n");
printf("%i \n",K[items][capacity]);
*/

/* Liberamos memoria */
   for (i = 0; i < items + 1; i++) {
  	free (K[i]);
   }
   free(K);


   return 1;
}


int DP_optimal(int capacity, int items, int * weights, int * values) {
   int i, c;
   int ** K;
   int cont= 0;
   int * col1;
   int * col2;
   int * colaux;
   int opt;

 
/* Reservamos memoria dinámica */
   K = (int **) malloc (2 * sizeof(int *));
	if (K == NULL) {
		printf ("Error al reservar memoria dinamica");
	}

   for (i = 0; i < 2; i++){
  	 K[i] = (int *) malloc ((capacity +1)*sizeof(int ));
		if (K[i] == NULL) {
			cont++;
			printf  ("Error al reservar memoria dinamica para el item %i. Error %i \n",i, cont);
			perror(" Error al reservar memoria dinamica");
		}
   }


   printf("Realizando DP_optimal correctament.... \n");

/* We only use 2 columns now:
	We always have to write on the 2nd one
	We always have to read from the first one
	At the end of each iteration we copy the first one into the second one.
	IMPROVEMENT: We dont "copy" the columns. We keep swithchin the columns with every item
*/

   col1 = K[0];
   col2 = K[1];
   for (i = 0; i <= items; i++){
	colaux = col1;
	col1 = col2;
	col2 = colaux;

       for (c = 0; c <= capacity; c++){
           if (i==0 || c==0) {
               col2[c] = 0;
	   }
           else if (weights[i-1] <= c)
                 col2[c] = max(values[i-1] + col1 [c-weights[i-1]],  col1[c]);
/* e choose the maximum beteen the same value of the last table 
and the value of every object plus the value os the last table ith enought
space left to put that object */
           else
                 col2[c] = col1[c];
       }
   }

   opt = col2[capacity];
   printf(" Optimo calculado: %i \n", opt);

/* Liberamos memoria */
   for (i = 0; i < 2; i++) {
  	free (K[i]);
   }
   free(K);

	return  opt;
}













