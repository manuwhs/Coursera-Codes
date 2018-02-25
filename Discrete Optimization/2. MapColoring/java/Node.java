
class Node {
	int number;	/* Number of the node */
	int color;	/* Color of the node */
	int n_colors;	/* Number of possible colors */
	int [] connected;	/* Conected connected nodes */
	int n_connected;	/* Number of nodes conected */
	int [] colors;		/* Possible colors the node can take */

	Node (int num, int n_nodes) {   /* Initialize a node with its number and void connected nodes */
		this.number = num;
		this.n_connected = 0;
	     	this.connected = new int [n_nodes];		/* Max number of possible conections */
		this.color = -1;
	}

	int add_connection (int node) {
		this.connected[this.n_connected] = node;
		this.n_connected += 1;
		return 0;
	}

	int set_colors (int num) {
		this.n_colors = num;		/* Possible colors */
		this.colors = new int [num];
		for (int i = 0; i < num; i++){
			this.colors[i] = i;
		}
		return 0;
	}

	int prune_feas (int color) {			/* It prunnes a given color from the possible color of a node */
		for (int i = 0; i < this.n_colors; i++) {
			if ( colors[i] == color ) {
				for (int j = i; j < this.n_colors -1; j++) {
					this.colors[j] = this.colors[j+1];
				}
			this.n_colors -=1 ;	/* Puta linea !!!!!!!!!!!!! */
			break;
			}
		}
		return this.n_colors;
	}
	
	int ran_choice () {
		int ran = (int) ( Math.random() * this.n_colors ); 
		return this.colors[ran];	/* Puta linea !!!!!!!!!!!!! */
	}
	
	int min_choice () {
		int min = colors[0];
		return min;
	}

}

