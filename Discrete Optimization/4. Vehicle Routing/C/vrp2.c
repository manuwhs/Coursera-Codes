#include <stdio.h>
#include <stdlib.h>
#include "funciones.h"
#include "vrp_funciones.h"
#include <math.h>
int main() {

    float ** points;
    float * X, * X_aux;
    float * Y, * Y_aux;
    float * C,	* C_aux;	/* Capacity demanded by the costumers */
    int * order;		/* Ordenar los nodes en funcion de X o Y */
    int ** capas;		/* Capas */
    int ** possibles;		/* For every node we will have an array of posible nodes to link */
    float ** distances;		/* Distances */	
    int *cap_size;		/* Tamano de las capas */
    int *pos_size;		/* Tamano de possibles */
    int ** car_costumers;	/* The array where we put the costumer that belongs to each car */
				/* car_costumers[n_cars_used] = Path os the cars visited by that car */
    int ** best_solutions;	/* Best solution paths ever got */
    int ** final_best;		/* Same as best_solutions but ordered so that the 0 is at the beggining */
    int * greedy_taken;		/* For the greedy, to know which costumers are already taken */

    int * n_costum_car;		/* It has the number of costumers every car has */
    int * n_costum_best;	/* It has the number of costumers every car has */
    float * cap_left;		/* It has the capacity left every car has */
    float * cap_left_best;
    int finish = 0;
    float * paths;		/* The distance that every car takes */
    float * bests;		/* The best distance that every car takes */
    float best = 0;		/* Best overall value */

    int layers;			/* Numero de capas */
    float T, penalty;
    int n_costum2;
    int total_cars;
    int parity;
    int pos;
    int iterations;
    float average_delta;

    int n_costum;		/* Numero de costumers */
    int n_cars;
    int car_capacity;
    int taken = 0;
    char fichero[] = {"./tmp.data"};

    int i,j,k,l,r, cont, aux_car, costum,c;			/*Contadores */

    points = (float **) malloc (3 * sizeof(float *));
    float path;
    float aux;
    get_costumers (fichero, &n_costum, &n_cars, &car_capacity, points) ;
    X = points[0];
    Y = points[1];
    C = points[2];


    X_aux = (float *) malloc (n_costum * sizeof(float));
    Y_aux = (float *) malloc (n_costum * sizeof(float));
    C_aux = (float *) malloc (n_costum * sizeof(float));

    copy_vector_float(X_aux, X, n_costum);
    copy_vector_float(Y_aux, Y, n_costum);
    copy_vector_float(C_aux, C, n_costum);

    for( i = 0; i < n_costum; i++) {
	printf("Nodo %i --> (%f, %f) %f \n",i, X[i],Y[i], C[i]);
    }


    order = (int *) malloc (n_costum * sizeof(int));
    layers = (int) sqrt(n_costum);

    printf ("Numero de capas: %i \n", layers);


    /* Generamos las capas */

    ordenar_float (X , order, n_costum);
    reordenar_float (Y, order, n_costum);
/*
    for( i = 0; i < n_costum; i++) {
	printf("%i ",order[i]);
    }
    printf("\n");
    printf("\n");
*/
/* Now they are ordered in decreasing value of X) */
    capas = get_layers (layers, n_costum, X, Y ,order, &cap_size);
    printf("Capas Done \n");

    for (i = 0; i < cap_size[0]; i++){
	for (j = 0; j < cap_size[i+1];j++){
		printf("%i ",capas[i][j]);
	}
	printf(" \n");
    }

/* Now we create the posibles for each node */
/* Since we ordered the nodes for building the nodes, we have to get back to the original */
    X = X_aux;
    Y = Y_aux;

    possibles = get_possible(capas, cap_size, 3, n_costum, &pos_size);
    printf("Possible Done \n");

    distances = get_distances ( X,  Y, possibles, pos_size);
    printf("Distances Done \n");
/*
    for (i = 0; i < n_costum; i++) {
   	printf("Nodo %i  --> %i\n", i,pos_size[i+1]);
	for (j = 0; j < pos_size[i+1]; j++){
		printf("%i ", possibles[i][j]);
	}
	printf("\n");
   }

*/
/*
To avoid reallocating memory the hole time we will create:
	- For every car an array with the length of every costumer.
	- An array that tells us the amount of people at every car.
*/
    total_cars = n_cars;
    n_costum_car = (int *) malloc (sizeof(int) * n_cars);
    n_costum_best = (int *) malloc (sizeof(int) * n_cars);
    cap_left = (float *) malloc (sizeof(float) * n_cars);
    cap_left_best = (float *) malloc (sizeof(float) * n_cars);
    paths = (float *) malloc (sizeof(float) * n_cars);
    bests = (float *) malloc (sizeof(float) * n_cars);

    for (i = 0; i < n_cars; i++) {
	cap_left[i] = car_capacity;	/* Initial remaining capacity */
	n_costum_car[i] = 1;		/* Coz every car starts with the 0 point */
	paths[i] = 0;
    }

    best_solutions = (int **) malloc (sizeof(int*) *n_cars);
    car_costumers = (int **) malloc (sizeof(int*) *n_cars);
    final_best = (int **) malloc (sizeof(int*) *n_cars);
    greedy_taken = (int *) malloc (sizeof(int *) * (n_costum));
    zero_int (greedy_taken, n_costum);

    for (i = 0; i < n_cars; i++ ) {
	car_costumers[i] = (int *) malloc ((n_costum + 1) * sizeof(int));
	best_solutions[i] = (int *) malloc ((n_costum + 1) * sizeof(int));
        final_best[i] = (int *) malloc ((n_costum + 1) * sizeof(int));

	car_costumers[i][0] = 0;	/* The first element will be always the warehouse and
					it will be the only element we will never change */
    }

    cont = 0;
    costum = 0;
    aux_car = -1;
    taken = 0;
/* Greedy */
/* The greedy itself doesnt matter but we should figure out a way to get the
    For the greedy solutions, what we are gonna do is:
    - Use dinamic programing to fill all the cars
    - Usa Local Search + Simulated Anneling to every car to get the best posible order.
*/

    ordenar_float (C + 1, order, n_costum - 1);	/* +1 to avoid warehouse */
    C = C_aux;
    printf("\n\n");
    for ( i = 0; i < n_costum - 1; i++) {
	printf("%i ", order[i]);
    }
    printf("\n\n");
    for ( i = 0; i < n_costum -1; i++) {		/* For every costumer */
	for (j = 0; j < n_cars; j++ ){
		if (cap_left[j] - C[order[i]+1] >= 0 ) {
//			printf(" order[i]+1--> %i", order[i]+1);
			car_costumers[j][n_costum_car[j]] = order[i]+1;
			cap_left[j] -= C[order[i]+1];
			n_costum_car[j] += 1;
			break;
		}
	}

    }
    for (i = 0; i < n_cars; i++ ) {
	if (n_costum_car[j] == 1){
		break;
	}
   } 
	n_cars = i;
    printf("Cars %i -> %i \n", aux_car, n_costum);

    for ( i = 0; i < n_cars; i++ ) {
	for (j = 0; j < n_costum_car[i]; j++){
		printf("%i ", car_costumers[i][j]);
	}
	printf("\n");
    }


    for (i = 0; i < n_cars; i++ ){
	paths[i] = get_path (X, Y, car_costumers[i], n_costum_car[i] );
	bests[i] = paths[i];
	copy_vector_int(best_solutions[i], car_costumers[i], n_costum_car[i]);
	best += bests[i];	
    }
    printf(" Lo mejón de lo mejón: %f \n", best);
    copy_vector_float(cap_left_best, cap_left, n_cars);
    
    /* First Idea:
	- First run the "best swap" algorithm for all the routes.
	- Then take one costumer from one car and give it to another car
	- Rerun the "best swap"
	- Redo all this until a given number of swaps.
*/
/* Lets try the best swap for everyone a couple of times and see if it works properly */
    T = 0.2;
    for (i = 0; i < n_cars; i++ ){	
	for (k = 0; k < 5; k++) {	
		for (j = 0; j < n_costum_car[i]; j++ ) {	
		
SA (j, X, Y, best_solutions[i], &bests[i], car_costumers[i] , &paths[i], T,n_costum_car[i]);
		}
	}
    }

    best = 0;
    path = 0;
    for (i = 0; i < n_cars; i++ ){
	best += bests[i];
	path += paths[i];
    }

    printf("Antes de los cambios \n");
    for ( i = 0; i < n_cars; i++ ) {
	for (j = 0; j < n_costum_car[i]; j++){
		printf("%i ", car_costumers[i][j]);
	}
	printf("\n");
    }

   T = 100;
   penalty = 1000000;

printf("CAMBIO ----------------_>\n");
	copy_vector_int (n_costum_best,n_costum_car, n_cars);
for (r = 0; r < 100; r++){
for (l = 0; l < 100; l++ ) {
	T = T*0.9999;
	change_car_SA (X, Y,distances, possibles, pos_size, best_solutions, &best, car_costumers , &path, T , n_cars, n_costum_car, penalty, cap_left, C,n_costum_best, cap_left_best);

}

    for (i = 0; i < n_cars; i++ ){	
	for (k = 0; k < 5; k++) {
		for (j = 0; j < n_costum_car[i]; j++ ) {		
SA (j, X, Y, best_solutions[i], &bests[i], car_costumers[i] , &paths[i], T,n_costum_car[i]);
		}
	}
    }
    best = 0;
    path = 0;
    for (i = 0; i < n_cars; i++ ){
	best += bests[i];
	path += paths[i];
    }

}
    printf("Despues de los cambios \n");
    for ( i = 0; i < n_cars; i++ ) {
	for (j = 0; j < n_costum_car[i]; j++){
		printf("%i ", car_costumers[i][j]);
	}
	printf("\n");
    }

    printf("Mejores del copon\n");
    for ( i = 0; i < n_cars; i++ ) {
	for (j = 0; j < n_costum_best[i]; j++){
		printf("%i ", best_solutions[i][j]);
	}
	printf("\n");
    }

   /* Since the 0 could be anywhere and it has to be the first one, we fix that */
   for (i = 0; i < n_cars; i++ ){
	pos = findint(best_solutions[i], n_costum_best[i], 0);	
	for (j = pos; j < n_costum_best[i]; j++ ) {
		final_best[i][j - pos] = best_solutions[i][j];
	}
	for (j = 0; j <= pos; j++ ){
		final_best[i][ n_costum_best[i] - pos + j] = best_solutions[i][j];	
	}
    }

    printf("Final---------------------------------\n");
    for ( i = 0; i < n_cars; i++ ) {
	for (j = 0; j < n_costum_best[i]; j++){
		printf("%i ", best_solutions[i][j]);
	}
	printf("\n");
    }


     printf("Best obtenido con cambios:	%f\n",best);
    best = 0;
    for (i = 0; i < n_cars; i++ ){
	bests[i] = get_path (X, Y, best_solutions[i], n_costum_best[i] );
	best += bests[i];
    }
     printf("Best real:	%f\n",best);

     path = 0;
     for (i = 0; i < n_cars; i++) {
        aux =(float) car_capacity;
	for (j = 0; j < n_costum_best[i]; j++ ){
		aux -= C[final_best[i][j]];
	}
	path += penalty * min (0, aux);
     }
	printf("Total penalty %f\n", path);

     print_vrp ( final_best, n_costum_best, total_cars , best, "out");

    /* Liberamos memoria */
    free (points[0]);
    free (points[1]);
    free (X);
    free (Y);

    free (points);
    free (order);

    for (i = 0; i < cap_size[0]; i++) {
	free (capas[i]);
    }
    free (capas);
    free (cap_size);
 

    for (i = 0; i < n_costum; i++){
	free(possibles[i]);
    }
    free(possibles);

    for (i = 0; i < n_costum; i++){
	free(distances[i]);
    }
    free(distances);

    free(pos_size);

    printf("Memoria liberada \n");
    return 1; 
}










