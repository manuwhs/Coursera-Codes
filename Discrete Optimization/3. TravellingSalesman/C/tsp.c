#include <stdio.h>
#include <stdlib.h>
#include "funciones.h"
#include "tsp_funciones.h"
#include <math.h>
int main() {

    float ** points;
    float * X, * X_aux;
    float * Y, * Y_aux;
    int * order;		/* Ordenar los nodes en funcion de X o Y */
    int ** capas;		/* Capas */
    int ** possibles;		/* For every node we will have an array of posible nodes to link */
    float ** distances;		/* Distances */
    int * solution, * best_solution;
    int *cap_size;		/* Tamano de las capas */
    int *pos_size;		/* Tamano de possibles */
    int layers;			/* Numero de capas */
    float T, k;
    int n_nodes2;
    int parity;
    int iterations;
    float average_delta;

    float best, path;
    int n_nodes;		/* Numero de nodos */

    char fichero[] = {"./tmp.data"};

    int i,j;			/*Contadores */

    points = (float **) malloc (2 * sizeof(float *));


    get_points (fichero, &n_nodes, points);
    X = points[0];
    Y = points[1];



    X_aux = (float *) malloc (n_nodes * sizeof(float));
    Y_aux = (float *) malloc (n_nodes * sizeof(float));

    copy_vector_float(X_aux, X, n_nodes);
    copy_vector_float(Y_aux, Y, n_nodes);
/*
    for( i = 0; i < n_nodes; i++) {
	printf("Nodo %i --> (%f, %f) \n",i, X[i],Y[i]);
    }
*/

    order = (int *) malloc (n_nodes * sizeof(int));
    layers = (int) sqrt(n_nodes);

    printf ("Numero de capas: %i \n", layers);


    /* Generamos las capas */

    ordenar_float (X , order, n_nodes);
    reordenar_float (Y, order, n_nodes);
/*
    for( i = 0; i < n_nodes; i++) {
	printf("%i ",order[i]);
    }
    printf("\n");
    printf("\n");
*/
/* Now they are ordered in decreasing value of X) */
    capas = get_layers (layers, n_nodes, X, Y ,order, &cap_size);
    printf("Capas Done \n");
/*
    for (i = 0; i < cap_size[0]; i++){
	for (j = 0; j < cap_size[i+1];j++){
		printf("%i ",capas[i][j]);
	}
	printf(" \n");
    }
*/
/* Now we create the posibles for each node */
/* Since we ordered the nodes for building the nodes, we have to get back to the original */
    X = X_aux;
    Y = Y_aux;

    possibles = get_possible(capas, cap_size, 3, n_nodes, &pos_size);
    printf("Possible Done \n");

    distances = get_distances ( X,  Y, possibles, pos_size);
    printf("Distances Done \n");
/*
    for (i = 0; i < n_nodes; i++) {
   	printf("Nodo %i  --> %i\n", i,pos_size[i+1]);
	for (j = 0; j < pos_size[i+1]; j++){
		printf("%i ", possibles[i][j]);
	}
	printf("\n");
   }
*/
/* Greedy */

    solution = (int *) malloc (n_nodes * sizeof(int));
    best_solution = (int *) malloc (n_nodes * sizeof(int));

    for (i = 0; i < n_nodes; i++) {
	solution[i] = i;
    }

    copy_vector_int (best_solution, solution, n_nodes );
    best = get_path (X, Y, solution, n_nodes );
    path = best; 
    printf("Greedy soluion done: %f \n", best);
/* SA tunning*/
/* For getting the temperature we get the average "delta" for the problem */
/* First of all we make a full SA with T = 0 */

    n_nodes2 = n_nodes/2;
    T = 10000000;

    for (i = 0; i < 2; i++) {

	parity = i % 2;
	for (j = 0; j < n_nodes2 - 1; j++) {

		SA (j*2 + parity, X, Y,distances, possibles, pos_size, best_solution, &best, solution, &path, T );
	}
    }
/* Now we try a very large T and see the average delta */
    T = 0.0000001;
    for (i = 0; i < 6; i++) {

	parity = i % 2;
	for (j = 0; j < n_nodes2 - 1; j++) {
		
		average_delta += SA (j*2 + parity, X, Y,distances, possibles, pos_size, best_solution, &best, solution, &path, T );
	} 
    }
        average_delta = average_delta /(6 * n_nodes);
	printf("Average delta: %f \n", average_delta);
// Posibly get a solution calculated before to keep working at that //

//	load_solution ("out",n_nodes, solution, &best);
//	path = best;
//	copy_vector_int(best_solution, solution, n_nodes);

// NOWWWWWWWWWWWWw
    printf("Performing SA\n");
    printf("\n");
    T = average_delta;
    k = 0.9995;
//    T = 10;
    iterations = 10000;
    for (i = 0; i < iterations; i++) {
    printf(" Realizando %i / %i \n",i + 1,iterations);
	T = T*k;
//	printf("T: %f \n", T);
	parity = i % 2;
	for (j = 0; j < n_nodes2 - 1; j++) {
		
		SA (j*2 + parity, X, Y,distances, possibles, pos_size, best_solution, &best, solution, &path, T );
	}
	printf("Path: %f \n", path);
    }

// Get to the local minima:

    printf("Getting to local minimum\n");
    for (i = 0; i < 4; i++) {
	parity = i % 2;
	for (j = 0; j < n_nodes2 - 1; j++) {
		best_swap (j*2 + parity, X, Y,distances, possibles, pos_size, best_solution, &best, solution, &path, T );
	}
	printf("Path: %f \n", path);
    }

    best = get_path (X, Y, best_solution, n_nodes );
    print_nodes (best_solution, n_nodes ,best, "out") ;
    printf(" ---------------> %f <-------------------- \n", best);
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
 

    for (i = 0; i < n_nodes; i++){
	free(possibles[i]);
    }
    free(possibles);

    for (i = 0; i < n_nodes; i++){
	free(distances[i]);
    }
    free(distances);

    free(pos_size);
    free (solution);
    free (best_solution);

    printf("Memoria liberada \n");
    return 1; 
}










