
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

node * create_node (char * branch , int value, int room, int estimate, int depth, int items);
void split_node (node * n, params * pa);
void del_node (params * pa);
char check_node (node * n, params * pa);
int BB (int capacity, int items, int * weights, int * values );
