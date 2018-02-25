
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

int  DP(int capacity, int items, int * weights, int * values, int * best, char * taken_out) {
   int i,j, c;
   int ** K;
   int aux;
   int desp, desp2;
   int n_columns;
   int flag_OK = 0;	// Flag para saber si la reserva ha ido mal o tenemos que reducir numero de columnas 
   int cont= 0;
   int i_c;		// items per column
   int r;		// Rest of the items per column
   char taken[items];
   int row, column; 	/* For trace-back */
 

/* Sometimes we cant make as many malloc as we can, even tho there is enough space to allocate the memory,
we are gona set the limit at 1000 and if it works we will have to make join items columns, which will
change the way we call them. Instead of using the [dir] we will add up the number of position of a column
which is capacity + 1 */

   n_columns = 1000;  // PARAMETRO INICIAL


while (flag_OK != 1 ) {
   flag_OK = 1;
   cont = 0;
   i_c  = items / n_columns;

  	 while(i_c == 0 ) {
		n_columns = n_columns/1.1;
		 i_c  = items / n_columns;
	}

   r = items % n_columns;

 /* We will add the extra column generated fot item 0 in the r-vector */

/* Reservamos memoria dinámica */
   K = (int **) malloc ((n_columns +1)*sizeof(int *));
	if (K == NULL) {
		printf ("Error al reservar memoria dinamica");
	}

/* Now we create the columns */
/* We keep allocation and freing memory until we get to a reacheable balance */

   for (i = 0; i < i_c + 1; i++){
	if (i != i_c) {
  		 K[i] = (int *) malloc (i_c *(capacity +1)*sizeof(int ));
			if (K[i] == NULL) {
				cont++;
				printf  ("Error al reservar memoria dinamica para el item %i. Error %i \n",i, cont);
				flag_OK = 0;
				break;
			}
   	}
        else {
  		 K[i] = (int *) malloc ((r + 1) *(capacity +1)*sizeof(int ));
			if (K[i] == NULL) {
				cont++;
				printf  ("Error al reservar memoria dinamica para el item %i. Error %i \n",i, cont);
				flag_OK = 0;
				break;
			}
   	}
	if (flag_OK == 0 ) {

		printf("Lets free the memory allocate so far");

		for(j = 0; j < i; j++) {
			free (K[i]);
		{
		free (K);
/* To get the new posible number of columns we see how many fails we had */

		n_columns = cont - 3;
}




   for (i = 0; i <= n_columns; i++){
	desp = i*(capacity + 1);
	desp2 = (i - 1) * i*(capacity + 1);
       for (c = 0; c <= capacity; c++){

           if (i==0 || c==0) {
               *(*(K + desp) + c) = 0;
	   }
           else if (weights[i-1] <= c)
                *(*(K + desp) + c) = max(values[i-1] + *(*(K + des2p) + c-weights[i-1]),  *(*(K + desp2) + c));
/* e choose the maximum beteen the same value of the last table 
and the value of every object plus the value os the last table ith enought
space left to put that object */
           else
                 *(*(K + desp) + c) = *(*(K + desp2) + c);
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

	* best  = *(*(K + n_columns) + capacity);

/* We start trace-back */



zero_char(taken,items);
aux = K[items][capacity];
column = items;
row = capacity;


/* K [column][row] */
for (i = 0; i < n_columns; i++) {


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


	printf("%i \n", *best);
	for (i = 0; i < items; i++) {
		printf("%i ", taken_out[i]);
	}
	printf("\n\n");

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


