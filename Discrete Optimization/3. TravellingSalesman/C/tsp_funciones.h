int ** get_layers (int layers, int n_nodes, float * X, float * Y , int *order, int ** capa_size);
int ** get_possible(int ** capas, int * cap_s, int num, int n_nodes, int ** pos_size) ;
float length (int n1, int n2, float * X, float * Y);
float get_path (float * X, float* Y, int * solution, int n_nodes );
int OTP2 (int pos1,  int pos2, int * solution, int n_nodes );
int SA (int pos_n, float * X, float * Y, float ** distances, int ** possibles, int * pos_s, int * best_points, float* best, int *solution,float *path, int T );
float ** get_distances (float* X, float* Y, int ** possibles, int * pos_s);
int best_swap (int pos_n, float * X, float * Y, float **distances, int ** possibles, int * pos_s, int * best_points, float* best, int *solution,float *path, int T );
