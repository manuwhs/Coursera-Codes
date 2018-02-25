#include <stdio.h>
#include <stdlib.h>
#include "funciones.h"
#include "vrp_funciones.h"
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


int SA (int pos_n, float * X, float * Y, int * best_points, float* best, int *solution , float *path, float T, int n_costumers){
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

	for (i = 0; i < n_costumers; i++) {

		pos2 = i;		// # Posicion del primer nodo del vertice 2 en la solucion
		node2 = solution[i];
//		printf("Posicion 2: %i \n", pos2);
		if (pos1 ==  n_costumers - 1){
			pos12 = 0;
		}
		else {
			pos12 = pos1 + 1;
		}
		if (pos2 ==  n_costumers - 1){
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
/*			printf("Ans ");
			for (j = 0; j < n_costumers; j++ ){
				printf("%i ", solution[j]);
			}
			printf("\n");
			printf("Des ");
*/			OTP2(pos1,pos2,solution,n_costumers);
/*			for (j = 0; j < n_costumers; j++ ){
				printf("%i ", solution[j]);
			}
			printf("\n");
*/			*path = *path - delta ;

			if (*path < *best){
				*best= *path;
				copy_vector_int (best_points, solution, n_costumers);
//				printf("Best: %f ----> %f\n", *best,get_path (X, Y, best_points, n_costumers));
/*				for (j = 0; j < n_costumers; j++){
					printf("%i ", best_points[j]);
				}
*/				
			}

		return abs(delta);	/* Means improvement */
		}
		prob = exp(delta/T);
		if ((prob > randomi )&&(dis > 1)) {
			OTP2(pos1,pos2,solution, n_costumers);
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



int change_car_SA (float * X, float * Y, float **distances, int ** possibles, int * pos_s, int ** best_points, float* best, int **solution , float *path, float T , int n_cars, int * n_costumers_car, float penalty, float *cap_left, float *C,int * n_costumers_best,float*cap_left_best) {
	/* This is what we will do:
		- Pick a random costumer (not the 0) from a car and try to put it in every other position
		- Use simulated anneling to check for the best 
*/
	int car1, pos1, pos1ant, pos1desp;
	int car2, pos2, pos2ant, pos2desp;	
	float ini, fin;
	float delta = 0.0, desp_delta= 0.0;
	float randomi, prob, ran_aux, ran_aux2;
	int i,j,k;
	int aux;
        float auxil, auxil2;
	
	/* Now we select a car and a costumer inside it and change it */
	car1 = (float)rand ()*n_cars/RAND_MAX;
	pos1 = (float)rand ()*n_costumers_car[car1]/RAND_MAX;

		if (pos1 == 0){
			pos1ant = n_costumers_car[car1] - 1;
		}
		else {
			pos1ant = pos1 - 1;
		}
		if (pos1 == n_costumers_car[car1] - 1){
			pos1desp = 0;
		}
		else {
			pos1desp = pos1 + 1;
		}

	car2 = (float)rand ()*n_cars/RAND_MAX;
	while (car2 == car1) {
		car2 = (float)rand ()*n_cars/RAND_MAX;
	}
	if (solution[car1][pos1] == 0) {
	//	printf("******************************************\n");
		return -1;
	}
/* 	0 8 3 2 12 5 7	->	0 8 3 12 5 7	-> Antes  3-2  y 2-12  -> Ahora 3-12
	0 13 4 9 17	->	0 13 2 4 9 17 	-> Antes  13-4	       -> Ahora 13-2 y 2-4
	We try to insert the object into every position of another car,

	 ___   ___   ____            ____   ___   ___
	|_3_| |_2_| |_12_| 	    |_13_| |_2_| |_4_|    
		|____________________pos2____|    pos2desp

	We use simulated anneling 
*/

	randomi = (float)rand ()/RAND_MAX;
//	printf(" Randomi %f \n", randomi);

	for (i = 0; i < n_costumers_car[car2] - 1 ; i++) {	/* For every possible point of insertion en car 2 */


		pos2 = i ;

//		printf("Posicion 2: %i \n", pos2);

		if (pos2 == n_costumers_car[car2] - 1){
			pos2desp = 0;
		}
		else {
			pos2desp = pos2 + 1;
		}
	
ini = length(solution[car1][pos1ant], solution[car1][pos1], X, Y) + length(solution[car1][pos1], solution[car1][pos1desp], X, Y);
ini += length(solution[car2][pos2], solution[car2][pos2desp], X, Y);

fin = length(solution[car2][pos2], solution[car1][pos1], X, Y) + length(solution[car1][pos1], solution[car2][pos2desp], X, Y);
fin += length(solution[car1][pos1ant], solution[car1][pos1desp], X, Y);

desp_delta =  ini - fin;

auxil = get_path(X,Y,solution[car1], n_costumers_car[car1]) + get_path(X,Y,solution[car2], n_costumers_car[car2]);

delta = desp_delta;
delta +=  -penalty*(min (0,cap_left[car1]) + min (0,cap_left[car2])) ;
delta -= -penalty *( (min (0,cap_left[car1] + C[solution[car1][pos1]])) +  (min (0,cap_left[car2]-C[solution[car1][pos1]])));

 //		printf("Delta: %f\n",delta);

		if  (delta >= 0) {
printf("******************************************\n");
//		        printf("Car1: %i \n", solution[car1][pos1]);
//			printf("Car2: %i %i \n",solution[car2][pos2],solution[car2][pos2desp]);
		/* Do the change */
/*-----------------------------------------------------------------------------------*/

		for (j = n_costumers_car[car2]; j > pos2; j--) {
			solution [car2][j+1] = solution[car2][j];
		}
		solution[car2][pos2+1] = solution[car1][pos1];
		n_costumers_car[car2] += 1;


		aux = solution[car1][pos1];
		for (j = pos1; j < n_costumers_car[car1]-1; j++){
			solution [car1][j] = solution[car1][j+1];
		}
		n_costumers_car[car1] -= 1;

auxil2 = get_path(X,Y, solution[car1], n_costumers_car[car1]) + get_path(X,Y,solution[car2], n_costumers_car[car2]);
printf("Delta real: %f y delta calculada: %f\n", auxil - auxil2, desp_delta);
    for ( k = 0; k < n_cars; k++ ) {
	for (j = 0; j < n_costumers_car[k]; j++){
		printf("%i ", solution[k][j]);
	}
	printf("\n");
    }
	cap_left[car1] += C[solution[car1][pos1]];
	cap_left[car2] -= C[solution[car1][pos1]];

printf("******************************************\n");
/*-----------------------------------------------------------------------------------*/
		*path = *path - desp_delta ;

			if (*path < *best){
				*best= *path;
				for ( j = 0; j < n_cars; j++ ) {	
					copy_vector_int (best_points[j], solution[j], n_costumers_car[j]);
				}
				copy_vector_int (n_costumers_best,n_costumers_car, n_cars);
				copy_vector_float(cap_left_best, cap_left, n_cars);
//				printf("NEW BESTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT\n");
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
		if (prob > randomi ) {
			*path = *path - desp_delta ;
printf("******************************************\n");
		        printf("Car1: %i \n", solution[car1][pos1]);
			printf("Car2: %i %i \n",solution[car2][pos2],solution[car2][pos2desp]);
		/*-----------------------------------------------------------------------------------*/

		for (j = n_costumers_car[car2]; j > pos2; j--) {
			solution [car2][j+1] = solution[car2][j];
		}
		solution[car2][pos2+1] = solution[car1][pos1];
		n_costumers_car[car2] += 1;


		aux = solution[car1][pos1];
		for (j = pos1; j < n_costumers_car[car1]-1; j++){
			solution [car1][j] = solution[car1][j+1];
		}
		n_costumers_car[car1] -= 1;
	cap_left[car1] += C[solution[car1][pos1]];
	cap_left[car2] -= C[solution[car1][pos1]];
    for ( k = 0; k < n_cars; k++ ) {
	for (j = 0; j < n_costumers_car[k]; j++){
		printf("%i ", solution[k][j]);
	}
	printf("\n");
    }
printf("******************************************\n");
/*-----------------------------------------------------------------------------------*/			*path = *path - delta ;
			return abs(delta);	/* Means improvement */
		}
	}
	return abs(delta);
}

int permutate_order(int * order, int n){
	int aux[n];
	int randomi;
	int taken[n];
	int i, j, ok;
	for (i = 0; i < n; i++){
		taken[i] = -1;
	}

	for (j = 0; j < n; j++) {
		ok = 0;
		while (ok != 1){
			ok = 1;
			randomi = ((rand ()*(float)n/RAND_MAX));
			for (i = 0; i < n; i++) {
				if (randomi == taken[i]){
					ok = 0;
				}	
			}
		}
		taken[j] = randomi;
	}
/*	for (i = 0; i < n; i++){
		printf("%i ", taken[i]);
	}	printf("\n");
*/
	for (i = 0; i < n; i++){
		order[i] = taken[i];
	}

	return 1;
}

















