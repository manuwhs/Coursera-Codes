
void zero_char (char * array, int length); 
void zero_int (int * array, int length);  

void get_items (char * data, int * capacity, int * items, int ** weights, int ** values); 
void get_items2 (char * archivo, int * capacity, int * items, int ** weights, int ** values);
void get_points (char * archivo, int * n_nodes, float ** points);
void load_solution (char * archivo, int n_nodes, int * solution, float * best);

void print_nodes (int * solution,int n_nodes ,float best, char * archivo);

void print_solution (char * solution,int items ,int best, char * archivo) ;

char * obtener_datos(char * archivo);  

int max(int a, int b);
float maxf (float * array, int num);  /* Give it the array and will give the best */

int dec2str(char  * cad, int digit);
int str2dec(char  * cad, char digit); 

int count_char(char * array, int len, int value);
int findint(int * array, int len, int value);

int ordenar_int (int * lista, int * orden, int len);
int ordenar_float (float * lista, int * orden, int len);

int reordenar_int (int * lista, int * orden, int len);
int reordenar_float (float * lista, int * orden, int len);

int desreordenar_char (char * lista, int * orden, int len); 


int copy_vector_char(char * duplicado, char * original, int num);
int copy_vector_int(int * duplicado, int * original, int num);
int copy_vector_float(float * duplicado, float * original, int num);


