
#include <stdio.h>
#include <stdlib.h>
#include "funciones.h"

/* Structure for every node */

typedef struct {
	char * branch ;
	int value;
	int room;
	int estimate;
	int depth;
	} node;

typedef struct {
	int * w;		// weights
	int * v;		// values
	node *** n;		// nodes matrix
	int n_nodes;		// number of pair [1 0] nodes in the matrix ----- Igual a n.depth
	int i;		// items
	int b;		// best solution so far
	char * t;		// taken objects
	char * aux_branch;
	} params;

node * create_node (char * branch , int value, int room, int estimate, int depth, int items) {
	node * nodeX;
	nodeX = (node *) malloc(sizeof(node));
	if (nodeX == NULL) {
		printf ("Error al reservar memoria dinamica para un Nodo");
	}
	nodeX->branch = (char *) malloc(sizeof(char)*items); 
	if (nodeX->branch == NULL) {
		printf ("Error al reservar memoria dinamica para el branch de un Nodo");
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
	/* We generate the new branch vector from the parent branch by copying it and addind 0 or 1 */
	copy_vector_char(pa->aux_branch, n->branch, n->depth);

	pa->aux_branch[n->depth] = 1;
	node_1 =  create_node(pa->aux_branch, n->value + pa->v[n->depth],n->room - pa->w[n->depth],n->estimate, n->depth + 1,pa->i);

	pa->aux_branch[n->depth] = 0;
	node_0 =  create_node(pa->aux_branch,n->value, n->room ,n->estimate -  pa->v[n->depth], n->depth + 1, pa->i);

	pa->n[n->depth][0] = node_1; 
	pa->n[n->depth][1] = node_0; 
	pa->n_nodes++;
}

void del_node (params * pa) {
	/* We have to free the 2 nodes of the branch and the branch parameter of those 2 branches */
	free (pa->n[pa->n_nodes-1][0]->branch);
	free (pa->n[pa->n_nodes-1][1]->branch);

	free (pa->n[pa->n_nodes-1][0]);
	free (pa->n[pa->n_nodes-1][1]);
	pa->n_nodes--;
	
}

char check_node (node * n, params * pa) {

	int i;



for(i = 0; i < n->depth; i++){
	printf("%i ", n->branch[i]);
	}
	printf("\n");



/* If the branch is no longer gonna get a better solution or room <0, we get back  */
	if (((n->estimate <= pa->b))||(n->room < 0)) {

		if (count_char(n->branch,n->depth, 0)== n->depth ){
			return 2;
		}

		if(n->branch[n->depth-1] == 0){
			printf ("Rama eliminada con profundidad %i",n->depth);
			copy_vector_char(pa->aux_branch, n->branch, n->depth);
			i = 0;
			while (pa->aux_branch[n->depth -1 -i] == 0){
				del_node (pa);
				i++;
			}
			return 0;
		}
		return 0;
	}

/* If we got to the bottom of the tree or the one before and we know that if we add a item then n-> room <0 */
	else if ((n->depth == pa->i)||((n->depth == pa->i-1)&&(n->room - pa->w[pa->i-1] < 0))){

		if (n->value > pa->b){

			printf ("New Best: %i \n",n->value);
			pa->b = n->value;
			copy_vector_char(pa->t, n->branch, n->depth);
		}

		copy_vector_char(pa->aux_branch, n->branch, n->depth);
		i = 0;
		del_node (pa);
		while (pa->aux_branch[n->depth -2 -i] == 0){
			del_node (pa);
			i++;
			if (i >= n->depth-1){
				return 2;
			}
		}
		return 0;
	}
	else {
		split_node (n,pa);
		return 1;
	}
}

int BB (int capacity, int items, int * weights, int * values ) {

	int i;
	node * node_X1, * node_X0;	/* First 2 nodes */
	params *pa;			/* Parameters that all func will share */
	int finish = 1;			/* Value to explore de tree */
	node *** nodes;		/* Matriz to place the node estructure 
					It's done so that we have to reember item nodes at most */ 
	int estimate = 100000000;		/* Estimation for the relaxation */			
	
/* Create de nodes matrix */
	nodes = (node ***)malloc(items * sizeof(node **));
	for (i = 0; i < items; i++ ){
		nodes[i] = (node **)malloc(2 * sizeof(node *));
	}

/* Set the Params structure */
	pa = (params *)malloc(sizeof(params));
	pa->w = weights;
	pa->v = values;
	pa->n = nodes;
	pa->i = items;
	pa->b = 0;			/* Initially, the best is 0 */
	pa->n_nodes = 1;		/* As we put the first par [1 0] nodes in the matriz, we have 1 node placed */

	pa->aux_branch = (char *)malloc(items*sizeof(char));	/* Auxiliar branch teller */
	zero_char (pa->aux_branch,items);

	pa->t = (char *)malloc(items * sizeof(char)); 		/*For storing the result's path */ 
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
/* At this point we have the solution in the params */
	printf("Resultados\n");
	printf("Valor máximo: %i \n", pa->b);
	for (i = 0; i < items; i++) {
		printf("%i ", pa->t[i]);
	}
	printf("\n");


/* Free dinamic stuff */
	free (pa->aux_branch);
	free (pa->t);
	free (pa);

	for (i = 0; i < items; i++ ){
		free(nodes[i]);
	}
	free (nodes);

	return 1;
}




















