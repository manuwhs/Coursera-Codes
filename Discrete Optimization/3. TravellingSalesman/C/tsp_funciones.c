#include <stdio.h>
#include <stdlib.h>
#include "funciones.h"
#include "tsp_funciones.h"
#include <math.h>

 int ** get_layers (int layers, int n_nodes, float * X, float* Y , int *order, int ** capa_size) {
	int N_p_l = n_nodes / layers;
	int rest = n_nodes % layers;
	int ** capas;
	int i = 0,j;
	int * cap_s;
	int order_aux [layers + 1];
	int pos = 0;	/* For coping the right positions in the layers */
	
	*capa_size = (int *) malloc ( (layers + 1)*sizeof(int));
	cap_s = *capa_size;	/* For makin code more clear */

	/* capa_size has the number of nodes every layer has, and the number of layers in its position 0 */
	cap_s[0] = layers;

	if (rest > 0 ) {
		for (i = 0; i < rest; i++) {
			cap_s[i+1] = N_p_l + 1;
		}
	}
	for (i = i; i < layers; i++) {
		cap_s[i+1] = N_p_l;
	}
	

	capas = (int **)malloc (sizeof(int *)*layers);

	for (i = 0; i < layers; i++) {

		capas[i] = (int	*) malloc (cap_s[i+1]*sizeof(int));


		for (j = 0; j < cap_s[i+1]; j++) {
			capas[i][j] = order[pos + j];
		}
		pos += cap_s[i+1];

		ordenar_float (Y + pos - cap_s[i+1], order_aux, cap_s[i+1]);
		reordenar_int(capas[i], order_aux, cap_s[i+1]);
	}
        return capas;
}








//-------------------------------------------------------------------------------------------------------------
/* n: Number of points in every direction we are gonna look at
# We get the posible points */

int ** get_possible(int ** capas, int * cap_s, int num, int n_nodes, int ** pos_size) {
	int i,j,k,l;	/* Contadores  */
	int n = 2*num + 1;
	int aux_possible[1000];	/* Auxiliar variable for possible points */
	int count;
	int node;	
	int * pos_s;
	
	int ** possibles;

	possibles = (int **) malloc (n_nodes*sizeof(int *));

	if (possibles == NULL ) {
		perror(" Error de memoria: ");
	}

	*pos_size = (int *) malloc ( (n_nodes + 1) * sizeof (int) );
	pos_s = *pos_size;	/* Has the possible of every node, pos_s[0] es el numero de nodes */
	if (pos_s == NULL ) {
		perror(" Error de memoria: ");
	}
	pos_s[0] = n_nodes;

	for (k = 0; k < cap_s[0]; k++) {	// For every layer
	   for (l = 0; l < cap_s[k +1]; l++){   // For every node of each layer
		node = capas[k][l];
		count = 0;

	      for (i = 0; i < n; i++){		// For every layer we are gonna check
		      for (j = 0; j < n; j++){

			if ( ((k + i - n/2) >= 0) && ((l + j - n/2) >= 0) ){	// Checking bounds
			if ( ((k + i - n/2) < cap_s[0]) && ((l + j - n/2) < cap_s[k + i - n/2 + 1] )){
				
				aux_possible[count] = capas[k + i - n/2][l + j - n/2];

				if (aux_possible[count] != capas[k][l]){
					count++;
				}
			}}
		      }
		}
		possibles[node] = (int *) malloc (count * sizeof(int));

		if (possibles[node] == NULL ) {
			perror(" Error de memoria: ");
		}
		pos_s[node + 1] = count;
		copy_vector_int (possibles[node], aux_possible, count);
	   }
	}

	return possibles;

}
//-------------------------------------------------------------------------------------------------------------
float length (int n1, int n2, float * X, float* Y) {
	return sqrt( (X[n1] - X[n2])*(X[n1] - X[n2]) + (Y[n1] - Y[n2])*(Y[n1] - Y[n2]) );
}	
//-------------------------------------------------------------------------------------------------------------

float get_path (float * X,float * Y, int * solution, int n_nodes ) {
	float obj = length ( solution[0], solution[n_nodes -1], X, Y);
	int i;
	for (i = 0; i < n_nodes -1; i++) {
		obj += length( solution[i], solution[i + 1], X, Y);
	}
	return obj;
}

//-------------------------------------------------------------------------------------------------------------


int OTP2 (int pos1,  int pos2, int * solution, int n_nodes ) {

	int i;
	int dis ;
	int aux;

	if (pos1 > pos2) {
		aux = pos1;
		pos1 = pos2;
		pos2 = aux;
	}
	pos1 += 1;

	if (pos2 - pos1 == 0) {
//		printf ("No hay cambio \n");
		return 0;
	}

	dis = abs(pos2 + 1 - pos1)/2 ;
	for (i = 0; i < dis; i++) {
		aux = solution[pos2 - i];
		solution[pos2 - i ] =  solution[pos1 + i];
		solution[pos1 + i ] = aux;
	}
	return 1;
}



//-------------------------------------------------------------------------------------------------------------


int SA (int pos_n, float * X, float * Y, float **distances, int ** possibles, int * pos_s, int * best_points, float* best, int *solution,float *path, int T ) {
	int node1, node2;
	int pos1, pos2;
	int pos12, pos22;
	int node12, node22;
	float ini, fin;
	float delta = 0.0;
	float randomi, prob;
	int i,j;
	int dis;
	
	pos1 = pos_n;
	node1 = solution[pos1];
	randomi = (float)rand ()/RAND_MAX;
//	printf(" Randomi %f \n", randomi);

	for (i = 0; i < pos_s[node1 + 1]; i++) {

		node2 = possibles[node1][i];
		pos2 = findint (solution, pos_s[0],node2);		// # Posicion del primer nodo del vertice 2 en la solucion

//		printf("Posicion 2: %i \n", pos2);
		if (pos1 == pos_s[0] - 1){
			pos12 = 0;
		}
		else {
			pos12 = pos1 + 1;
		}
		if (pos2 == pos_s[0] - 1){
			pos22 = 0;
		}
		else{
			pos22 = pos2 + 1;
		}
		
		node12 = solution[pos12];
		node22 = solution[pos22];

		ini = length(node1, node12, X, Y) + length(node2, node22, X, Y);
		fin = length(node1, node2, X, Y) + length(node12 , node22, X, Y);
//		printf (" %f <---> %f \n", distances[node1][i], length(node1, node2, X, Y));
//		printf (" Nodos: %i - %i \n", node1, node2);
		// distances[node1][i]
		dis = abs(pos1 - pos2);
		delta = ini - fin;	
//		printf("Delta: %f\n", delta);

		if  ((delta >= 0)&&(dis > 1)) {

			OTP2(pos1,pos2,solution,pos_s[0]);

			*path = *path - delta ;

			if (*path < *best){
				*best= *path;
				copy_vector_int (best_points, solution, pos_s[0]);
/*				printf("Best: %f ----> %f\n", *best,get_path (X, Y, best_points, pos_s[0]));
				for (j = 0; j < pos_s[0]; j++){
					printf("%i ", best_points[j]);
				}
				printf("\n");
*/
			}

		return abs(delta);	/* Means improvement */
		}
		prob = exp(delta/T);
		if ((prob > randomi )&&(dis > 1)) {
			OTP2(pos1,pos2,solution, pos_s[0]);
			*path = *path - delta ;
			return abs(delta);	/* Means improvement */
		}
	}
	return abs(delta);
}


//---------------------------------------------------------------------------------------------------------------- //

float ** get_distances (float* X, float* Y, int ** possibles, int * pos_s) {
	int i, j;
	float ** distan;

	distan = (float **) malloc (pos_s[0] * sizeof(float *));
	
	for (i = 0; i < pos_s[0]; i++) {
		distan[i] = (float *) malloc (pos_s[i+1] * sizeof(float));
		for (j = 0; j < pos_s[i+1]; j++) {
			distan[i][j] = length (i, possibles[i][j], X, Y); 
		}
	}
	return distan;
}
//---------------------------------------------------------------------------------------------------------------- //
int best_swap (int pos_n, float * X, float * Y, float **distances, int ** possibles, int * pos_s, int * best_points, float* best, int *solution,float *path, int T ) {
	int node1, node2;
	int pos1, pos2;
	int pos12, pos22;
	int node12, node22;
	float ini, fin;
	float delta = 0, improve;
	int i;
	int dis, final = -1;
	
	pos1 = pos_n;
	node1 = solution[pos1];

	improve = 0.0 ;
	for (i = 0; i < pos_s[node1 + 1]; i++) {

		node2 = possibles[node1][i];
		pos2 = findint (solution, pos_s[0],node2);		// # Posicion del primer nodo del vertice 2 en la solucion

//		printf("Posicion 2: %i \n", pos2);
		if (pos1 == pos_s[0] - 1){
			pos12 = 0;
		}
		else {
			pos12 = pos1 + 1;
		}
		if (pos2 == pos_s[0] - 1){
			pos22 = 0;
		}
		else{
			pos22 = pos2 + 1;
		}
		
		node12 = solution[pos12];
		node22 = solution[pos22];

		ini = length(node1, node12, X, Y) + length(node2, node22, X, Y);
		fin = length(node1, node2, X, Y) + length(node12 , node22, X, Y);
//		printf (" %f <---> %f \n", distances[node1][i], length(node1, node2, X, Y));
//		printf (" Nodos: %i - %i \n", node1, node2);
		// distances[node1][i]
		dis = abs(pos1 - pos2);
		delta = ini - fin;	
//		printf("Delta: %f\n", delta);

		if  ((delta >= improve)&&(dis > 1)) {
			final = i;
			improve = delta;
		}
	}
	if (final != -1) {
		node2 = possibles[node1][final];
		pos2 = findint (solution, pos_s[0],node2);		// # Posicion del primer nodo del vertice 2 en la solucion

		OTP2(pos1,pos2,solution,pos_s[0]);
		*path = *path - improve ;
		*best = *path;
		copy_vector_int (best_points, solution, pos_s[0]);
	}
	return 1;
}
//---------------------------------------------------------------------------------------------------------------- //






















