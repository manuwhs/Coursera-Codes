
#include "funciones.h"
#include <stdio.h>
#include <stdlib.h>


/*------------------------------------------------------------------------------------------------ */


/*------------------------------------------------------------------------------------------------ */
/* Normal Knapsak bottom - up */

int  DP(int capacity, int items, int * weights, int * values ) {
   int i, c;
   int ** K;
   int aux;
   int taken[items];
   int row, column; 	/* For trace-back */
 
/* Reservamos memoria dinámica */
   K = (int **) malloc ((items +1)*sizeof(int *));
	if (K == NULL) {
		printf ("Error al reservar memoria dinamica");
	}
   for (i = 0; i < items + 1; i++){

  	 K[i] = (int *) malloc ((capacity +1)*sizeof(int ));
		if (K == NULL) {
			printf ("Error al reservar memoria dinamica");
		}
   }
printf (" Memoria reservada bien ------------------------ \n");


   for (i = 0; i <= items; i++){
       for (c = 0; c <= capacity; c++){

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

/* We start trace-back */

zero_int(taken,items);
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

for (i = 0; i < items; i++) {
	printf ("%i ",taken[i]);
	}
	printf("\n");
printf("%i \n",K[items][capacity]);


/* Liberamos memoria */
   for (i = 0; i < items + 1; i++) {
  	free (K[i]);
   }
   free(K);


   return 1;
}


