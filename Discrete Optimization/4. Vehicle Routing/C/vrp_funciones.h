int ** get_layers (int layers, int n_nodes, float * X, float * Y , int *order, int ** capa_size);
int ** get_possible(int ** capas, int * cap_s, int num, int n_nodes, int ** pos_size) ;
float length (int n1, int n2, float * X, float * Y);
float get_path (float * X, float* Y, int * solution, int n_nodes );
int OTP2 (int pos1,  int pos2, int * solution, int n_nodes );
int SA (int pos_n, float * X, float * Y, int * best_points, float* best, int *solution , float *path, float T, int n_costumers);
float ** get_distances (float* X, float* Y, int ** possibles, int * pos_s);
int best_swap (int pos_n, float * X, float * Y, float **distances, int ** possibles, int * pos_s, int * best_points, float* best, int *solution,float *path, int T );
int change_car_SA (float * X, float * Y, float **distances, int ** possibles, int * pos_s, int ** best_points, float* best, int **solution , float *path, float T , int n_cars, int * n_costumers_car, float penalty,float*cap_left, float *C,int * n_costumers_best,float*cap_left_best);

int permutate_order(int * order, int n);
