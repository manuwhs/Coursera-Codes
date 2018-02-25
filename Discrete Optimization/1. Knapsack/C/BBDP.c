
#include <stdio.h>
#include <stdlib.h>
#include "funciones.h"
#include "BBDP.h"


node * create_node (char * branch , int value, int room, int estimate, int depth, int items) {
	node * nodeX;
	nodeX = (node *) malloc(sizeof(node));
	if (nodeX == NULL) {
		perror ("Error al reservar memoria dinamica para un Nodo");
	}
	nodeX->branch = (char *) malloc(sizeof(char)*items); 
	if (nodeX->branch == NULL) {
		perror ("Error al reservar memoria dinamica para el branch de un Nodo");
	}

	nodeX->value = value;
	nodeX->room = room;
	nodeX->estimate = estimate;
	nodeX->depth = depth;
	copy_vector_char(nodeX->branch, branch, depth);
	return nodeX;
}

/* Creates the next two nodes from a node and adds it to the end of the nodes list */
void split_node (node * n, params * pa){
	node * node_1, * node_0;		/*Pointers to the new nodes */
	/* We generate the new branch vector from the parent branch by copying it and addind 0 for one branch
	and 1 to the other */
	copy_vector_char(pa->aux_branch, n->branch, n->depth);

	pa->aux_branch[n->depth] = 1;
	node_1 =  create_node(pa->aux_branch, n->value + pa->v[n->depth],n->room - pa->w[n->depth],n->estimate, n->depth + 1,pa->i);

	pa->aux_branch[n->depth] = 0;
	node_0 =  create_node(pa->aux_branch,n->value, n->room ,n->estimate -  pa->v[n->depth], n->depth + 1, pa->i);

	pa->n[n->depth][0] = node_1; 
	pa->n[n->depth][1] = node_0; 
	pa->n_nodes++;
}
/* -------------------------------------------------------------------------------------------------------*/
void del_node (params * pa) {
	/* We have to free the 2 nodes of the branch and the branch parameter of those 2 branches */
	free (pa->n[pa->n_nodes-1][0]->branch);
	free (pa->n[pa->n_nodes-1][1]->branch);

	free (pa->n[pa->n_nodes-1][0]);
	free (pa->n[pa->n_nodes-1][1]);
	pa->n_nodes--;
	
}

/* -------------------------------------------------------------------------------------------------------*/
int del_branch (params * pa, char * branch, int depth, char num) {
	int i = 0;
	copy_vector_char(pa->aux_branch, branch, depth);

	del_node(pa);	/* In case the first 1 is a " 1 " */
	
	if (depth == 1) {
		return 2;
	}

	while (pa->aux_branch[depth -2 -i] == 0){
		del_node (pa);
		i++;
	}
	if (i == depth - 1){
		printf("Terminado por: %i \n", num);
		return 2;
	}
	return 0;
}
/* -------------------------------------------------------------------------------------------------------*/
/* -------------------------------------------------------------------------------------------------------*/
/* -------------------------------------------------------------------------------------------------------*/

char check_node (node * n, params * pa) {

	int i,j;
	int best = 0;
	int possible_best;
	int good = 0;
	int num_MBytes = 1000;
	int pos_per_MByte = 1000000 / sizeof(int);
	double MBytes_usados;

// Print the branch we are evaluating
for(i = 0; i < n->depth; i++){
	printf("%i ", n->branch[i]);
	}
	printf (" \n");
/* We have removed the estimation condition from the normal BB */
	if (n->room < 0) {	

/* We dont need the next code because if there is no estimation value that decreases when you choose
not to pick an object you will never get here from a 0 branch of a node */

		return 0;
	}
/* In this case very likely we are never gonna get to the end of the tree so we remove this code */

/*	if (n->value == pa->o){

		pa->b = n->value;
		copy_vector_char(pa->t, n->branch, pa->i);
		return 2;
	}
*/

/* The idea is:
Whenever we add an object the room left in the node (knapsack) will decrease,
when the product (Items_left * room_left) is less than a certain value so that
we can run de Dynamic Programming Algorithm we do it. 
This will calculate the best value that node will ever get.
We send to the algorithm the room left and the remaining objects.
After that, we compare with the best we have got so far and keep the biggest.
Then we return 0 so that it will check the condition if we didnt take that last object
and we start over taking the next object.
We have the problem that we are doing at least items DP operations but thats the price
 */

/* We check if we can use DP with the rest of that node */

/* If its imposible we get optimal from this configuration */

	if(n->branch[n->depth-1] == 0){
		possible_best = upper_bound(pa->w, pa->v, pa->i, n->room, n->value, n->depth);
//		printf(" Posible mejor %i \n",possible_best);
		if (possible_best < pa->o) {
			printf("Eliminado por BOUND -----------------------------------------------------------------------\n");
			return del_branch (pa, n->branch, n->depth, 0);
		}	
	}
	MBytes_usados = (float)(n->room +1) * (pa->i - n->depth + 1)/pos_per_MByte;
	if ( (int)MBytes_usados < num_MBytes*2) {
		printf("Realizando DP con demanda de: %i MBytes\n", (int)MBytes_usados);
		good = DP (n->room, pa->i - n-> depth, (pa->w + n->depth), pa->v + n->depth , &best, n->branch + n->depth);
		if (good == -1) {
			printf ("Error de memoria en el DP\n");
			return 2;
		}
		if ((best + n->value) > pa->b){
			printf ("New Best: %i \n",best + n->value);
			pa->b = best + n->value;
			copy_vector_char(pa->t, n->branch, pa->i);

			if (pa->b == pa->o){
				printf ("Encontrao por DP\n");
				return 2;
			}
		}

		/* Since all the brach is done, we go back until we find one taken object "1" and explore the "0"
		option of that object. Notice that if the last character is 1, we keep branching without deleting */

/* Notice that the DP can run for the branchs terminated with 0 as well, this wouldnt have any sense cause if we couldnt
do the DP taking the object, we wont be able to do it not taking it. 
But we are decreasing the number of objects so it could be posible that a ending 0 branch does an DP
Notice that if we an only do it with the ending "1", we will run at least "item" DP !!! */

		if(n->branch[n->depth-1] == 0) {
			return del_branch (pa, n->branch, n->depth, 1);
		}	
	return 0;	

	}

/* As a dimension of more than 10 would be too much we miss some values with this */

	else if (n->depth >= 200){

		return del_branch (pa, n->branch, n->depth, 1);
	}	
	
	/* If we got to the bottom of the tree */

	else if (n->depth == pa->i){

		if (n->value > pa->b){
			printf ("New Best: %i \n",n->value);
			pa->b = n->value;
			copy_vector_char(pa->t, n->branch, n->depth);
		}
		return 2;
	}
	
	/* If we coulnd make the DP, and everything OK, we keep taking objects */
	
	else {
		split_node (n,pa);
		return 1;
	}
}
/* -------------------------------------------------------------------------------------------------------*/
/* -------------------------------------------------------------------------------------------------------*/
/* -------------------------------------------------------------------------------------------------------*/
int BBDP (int capacity, int items, int * weights, int * values ) {

	int i;
	node * node_X1, * node_X0;	/* First 2 nodes */
	params *pa;			/* Parameters that all func will share */
	int finish = 1;			/* Value to explore de tree */
	node *** nodes;		/* Matriz to place the node estructure 
					It's done so that we have to reember item nodes at most */ 
	int optimal;		/* Estimation for the relaxation */	
	int estimate = 100;
	int orden[items];		
	float * density;
 
/* Create de nodes matrix */
	nodes = (node ***)malloc(items * sizeof(node **));
	if (nodes == NULL) {
		perror(" Error al reservar el arbol de nodos");
	}

	for (i = 0; i < items; i++ ){
		nodes[i] = (node **)malloc(2 * sizeof(node *));
		if (nodes[i] == NULL) {
			perror("Error al reservar el arbol de nodos");
		}
	}

/* Create the array of density values */
	density = (float *)malloc(items * sizeof(float));
	if (density == NULL) {
		perror(" Error al reservar la densidad");
	}

	for (i = 0; i < items; i++) {
		density[i] = (float) values[i]/weights[i];
	}
/* IMPROVEMENT:
We orden the object in decreasing order of weight so that we can start doind DP as soon as posible
We will have to change the order of the values acordingly
At the end of the program we reorder the list of taken objects */

/* We will order them in order of decreasion value/weight
The upper bound of the value is given using relaxation --> We can take fractional objects.
If we choose not to take an object (starting by the most value/weight), this upper bound value
for the problem will be ecual or minor to the one taking that object.
This upper bound will be the best solution we will ever get if we dont take the object and its very
easy to calculate so, if we say this upper bound has to be greater than the best solution,
we should be able to prune very fast and getting to the optimal value.

To calculate the optimal value we use DP but only keeping the last 2 rows so that the problem wont take
much memory, but we wont know the value of this one.


*/
	ordenar_float (density, orden, items);  // Ordenamos por densidad
	reordenar_int (values, orden, items);	// Reordenamos peso y valor en funcion de la densidad
	reordenar_int (weights, orden, items);

/*	for (i = 0; i < items; i++ ){
		printf("%i - %i: %f\n",values[i],weights[i], density[i]);
	}
	printf("\n");
*/
	optimal = DP_optimal(capacity,items, weights, values);
//	optimal = 1099893;
/* Set the Params structure */
	pa = (params *)malloc(sizeof(params)); 
	if (pa == NULL) {
		perror(" Error al reservar los parametros");
	}

	pa->w = weights;
	pa->v = values;
	pa->n = nodes;
	pa->i = items;
	pa->b = 0;			/* Initially, the best is 0 */
	pa->o = optimal;
	pa->n_nodes = 1;		/* As we put the first par [1 0] nodes in the matriz, we have 1 node placed */

	pa->aux_branch = (char *)malloc(items*sizeof(char));	/* Auxiliar branch teller */
	if (pa->aux_branch == NULL) {
		perror(" Error al reservar los parametros");
	}
	zero_char (pa->aux_branch,items);

	pa->t = (char *)malloc(items * sizeof(char)); 		/*For storing the result's path */ 
	if (pa->t == NULL) {
		perror(" Error al reservar los parametros");
	}
	zero_char (pa->t,items);

printf("Parámetros realizados \n");

/* We create the first two nodes */
	pa->aux_branch[0] = 1;
	node_X1 =  create_node(pa->aux_branch, pa->v[0], capacity - pa->w[0], estimate, 1, items);

	pa->aux_branch[0] = 0;
	node_X0 =  create_node(pa->aux_branch,0 , capacity , estimate -  pa->v[0], 1, items);

printf("Primeros 2 nodos creados \n");
	pa->n[0][0] = node_X1; 
	pa->n[0][1] = node_X0; 

printf("Nodos puestos en el array \n");

/* Iterative loop to go through the nodes */

    while (finish != 2) {
	if (finish == 1){
      	   finish = check_node (pa->n[(pa->n_nodes)-1][0], pa);
	}
	if (finish == 0){
           finish = check_node (pa->n[(pa->n_nodes)-1][1], pa);
	}
     }

/* Reordenamos el array como es debido */

/*
for (i = 0; i < items; i++) {
		printf("%i ", pa->t[i]);
	}
	printf("\n");
*/

	desreordenar_char (pa->t, orden, items);




/* At this point we have the solution in the params */
	printf("\n\nResultados:\n");
	printf("Valor máximo: %i \n", pa->b);
	for (i = 0; i < items; i++) {
		printf("%i ", pa->t[i]);
	}
	printf("\n");
/* Write the output */

print_solution (pa->t, pa->i ,pa->b, "out") ;

/* Free dinamic stuff */

	/* In case we didnt have to explore the whole tree */
	if (pa->n_nodes > 0){
		for (i = 0; i < pa->n_nodes; i++){
			del_node(pa);
		}
	}

	free (pa->aux_branch);
	free (pa->t);
	free (pa);

	for (i = 0; i < items; i++ ){
		free(nodes[i]);
	}
	free (nodes);
	free (density);

	return 1;
}





