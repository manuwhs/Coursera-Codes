// A Dynamic Programming based solution for 0-1 Knapsack problem
#include <stdio.h>
#include <stdlib.h>
#include "funciones.h"
#include "BB.h"
#include "DP.h"
 
// Returns the maximum value that can be put in a knapsack of capacity W
int BB (int capacity, int items, int * weights, int * values );
 
int main() {

    int i;
    int * weights;
    int * values;
    int capacity;
    int items;
    char fichero[] = {"./tmp.data"};
    char * data;
    int final;

    data = obtener_datos(fichero);
    get_items (data, &capacity, &items, &weights, &values);

/*
for( i = 0; i < items; i++) {
	printf("Objeto %i, Valor: %i, Peso: %i \n",i,values[i],weights[i]);
}
*/


    final = DP(capacity, items, weights, values);
 //   final = BB(capacity, items, weights, values);

    printf("PROGRAMA C ACABADO CON NORMALIDAD %i \n",final);

    /* Liberamos memoria */
    free (data);
    free (weights);
    free (values);
 
    return 1;
}



