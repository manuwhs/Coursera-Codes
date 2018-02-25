import java.io.*;

class Esfera {
	double radio;
	double area( ) {
		return 4.0 * 3.14159 * radio * radio;
	}
}

class Coloring {

	static int choose_node (Node [] nodes, int [] uncolored, int n_uncolored) {
		int ran = (int) ( Math.random() * n_uncolored );	/* Random */
		int aux = 10000, aux_i = 0;
		for (int i = 0; i < n_uncolored; i++ ) {
			if (nodes[uncolored[i]].n_colors < aux ) {
				aux = nodes[uncolored[i]].n_colors;
				aux_i = i;				/* Less colors */
			}
		}
		return uncolored[aux_i];					
	}

	/* This function colors a node, prune feasibily and check feasibility */
	/* It returns:		-1 if the colored node caused the thing to be infeasible
		   		-2 if the colored node was feasible but no node can be pruned
				0 - n_nodes: Node that can be prune coz it can only take one color 
*/
	static int color_node (Node [] nodes, int node, int [] uncolored, int n_uncolored, int flag) {
		int [] conections = nodes[node].connected;
		int feas, pruned;
		int color;
		if (flag == 0) {
			color = nodes[node].min_choice();
		}
		else {
			color = nodes[node].ran_choice();
		 }
		nodes[node].color = color;

/*		System.out.println("Prunning Node: " + node + " with color " + color +" Con conexiones: ");
		for (int i = 0; i < nodes[node].n_connected; i++ ) {
			if (nodes[conections[i]].color == -1) {
				System.out.print(conections[i] + " ");
			}
		}
		System.out.print("\n");
*/
		pruned = -2;
		for (int i = 0; i < nodes[node].n_connected; i++ ) {	/* We prune that color from the connections */
			if (nodes[conections[i]].color == -1) {
				feas = nodes[conections[i]].prune_feas(color);
				
				if (feas == 0) {
//					System.out.println("Nodo: " + conections[i] + " sin colores");
					return -1;
				}
				if (feas == 1) {
					pruned = conections[i];
				}
			}
		}
		/* We remove the colored node from the list of uncolored nodes */
/*		System.out.println("Antes");
		for (int i = 0; i < n_uncolored; i++ ) {
			System.out.println(uncolored[i]);
		}
*/
		for ( int i = 0; i < n_uncolored; i++ ) {
			if ( uncolored[i] == node ) {
				for (int j = i; j < n_uncolored -1; j++) {
					uncolored[j] = uncolored[j + 1];
				}
				break;
			}
		}
/*		System.out.println("Despues");
		for (int i = 0; i < n_uncolored - 1; i++ ) {
			System.out.println(uncolored[i]);
		}
*/
		return pruned;
	}


	static int initial_feasibility (Node [] nodes, int [] uncolored, int n_uncolored) {
		for (int i = 0; i < n_uncolored; i++ ) {
			if ( nodes[i].n_colors == 0 ) {
				return -1;
			}
		}
		return 0;
	}



public static void main( String args[] ) {
	int n_nodes = 0;
	int n_connections = 0;
	int node_to_color = -2;

	int [] uncolored;	/* List of uncolored nodes */
	int n_uncolored = 0;		/* Number of uncolored nodes */
	Node [] nodes;
	String FILE_NAME = "tmp.data";
	int [] aux = new int [10];	/* For not getting the error */
	int [] con_1 = aux;
	int [] con_2 = aux;
	int [] solution = aux;
	int final_colors = 10000;
	int aux_colors = 0;
	int unfeas;

	/*----------------------------- READ THE NODES ------------------------------------*/

try{
			  // Open the file that is the first 
			  // command line parameter
  FileInputStream fstream = new FileInputStream(FILE_NAME);
  			// Get the object of DataInputStream
  DataInputStream in = new DataInputStream(fstream);
  BufferedReader br = new BufferedReader(new InputStreamReader(in));
  String strLine;
 			 //Read File Line By Line
  strLine = br.readLine();
  String [] items = strLine.split(" ");
  n_nodes = Integer.parseInt(items[0]);
  n_connections = Integer.parseInt(items[1]);

  con_1 = new int [n_connections];
  con_2 = new int [n_connections];

  for (int i = 0; i < n_connections; i++)  {
	strLine = br.readLine();
	items = strLine.split(" ");
  	con_1[i] =  Integer.parseInt(items[0]);
  	con_2[i] =  Integer.parseInt(items[1]);
//  System.out.println ("Linea: " + con_1[i] +"/ " + con_2[i]);
  }
 			 //Close the input stream
  in.close();
    }catch (Exception e){//Catch exception if any
  System.err.println("Error: " + e.getMessage());
  }

	/*----------------------------- INITIALIZE NODES ------------------------------------*/
	n_uncolored = n_nodes;
 	uncolored = new int [n_nodes];
	nodes = new Node[n_nodes];
	solution = new int [n_nodes];

	for (int i = 0; i < n_nodes; i++ ) {
		uncolored[i] = i;
		nodes[i] = new Node(i,n_nodes);
		nodes[i].set_colors(n_nodes);
	}

	for (int i = 0; i < n_connections; i++ ) {
//		System.out.println ("Linea: " + con_1[i] +"/ " + con_2[i]);
		nodes[con_1[i]].add_connection (con_2[i]);
		nodes[con_2[i]].add_connection (con_1[i]);
	}
/*	for (int i = 0; i < n_nodes; i++ ) {
		System.out.println ("Nodo " + i);
		for (int j = 0; j < nodes[i].n_connected; j++ ) {
			System.out.println ( nodes[i].connected[j]);
		}
	}
*/
	/* We are gonna create a list with the "uncolored" nodes that we have to operate with and when
	we color them we remove them from it */

	/*----------------------------- FIRST RUN ------------------------------------*/

/* Strategy:	
	Start by running the algorithm once setting a huge possible colors number so that we get a feasible
	upper bound and then run the algorith several times until a given number of colors isnt feasible.
*/
	node_to_color = -2;	/* Coz initially no node can be pruned */
	n_uncolored = n_nodes;
	for (int i = 0; i < n_nodes; i++ ) {
		uncolored[i] = i;
		nodes[i].color = -1;
		nodes[i].set_colors(n_nodes);		/* Number of possible colors */
	}

	for ( int i = 0; i < n_nodes; i++ ) {

		if (node_to_color == -2) {
			node_to_color = choose_node (nodes, uncolored,  n_uncolored);
		}
		node_to_color = color_node (nodes,node_to_color, uncolored, n_uncolored,0);
		n_uncolored -= 1;
		if (node_to_color == -1) {
			unfeas = 1;
			break;
		}
	}

	aux_colors = 0;
	for (int i = 0; i < n_nodes; i++ ) {
		if (aux_colors < nodes[i].color) {
			aux_colors = nodes[i].color;
		}
//		System.out.println (solution[i]);
	}
	if (aux_colors < final_colors ) {
		final_colors = aux_colors;
		System.out.println ("New Best: " + final_colors);
		for (int i = 0; i < n_nodes; i++ ) {
			solution[i] = nodes[i].color;
//			System.out.println (solution[i]);
		}
	}

	/*NOW WE HAVE AN INITIAL GREEDY SOLUTION, NOW WE KEEP REDUCING THE NUMBER OF POSSIBLE COLORS */

	/*----------------------------- DO THE CONSTRAINT ------------------------------------*/

	int unsucces = 0;
	while (unsucces == 0 ) {
		unsucces = 1;

	for ( int k = 0; k < 1000000; k++ ) {
	/* Reinitilize to do it again */
		node_to_color = -2;	/* Coz initially no node can be pruned */
		unfeas = 0;
		n_uncolored = n_nodes;
		for (int i = 0; i < n_nodes; i++ ) {
			uncolored[i] = i;
			nodes[i].color = -1;
			nodes[i].set_colors(99);	// Final_colors//	/* Number of possible colors */
		}
//		System.out.println("K-> "+ k);

		for ( int i = 0; i < n_nodes; i++ ) {

	/*		System.out.println("Iteration: "+ i);
			for (int l = 0; l < n_nodes; l++) {
				if (nodes[l].color == -1) {
					System.out.print("Nodo " + l + " -> ");
					for (int j = 0; j < nodes[l].n_colors; j++ ) {
						System.out.print(nodes[l].colors[j] + " ");
			
					}
					System.out.print("\n");
				}
			}
	*/
			if (node_to_color == -2) {
				node_to_color = choose_node (nodes, uncolored,  n_uncolored);
			}
			node_to_color = color_node (nodes,node_to_color, uncolored, n_uncolored,1);
			n_uncolored -= 1;
			if (node_to_color == -1) {
				unfeas = 1;
				break;
			}
		}

		/*----------------------------- PREPARE SOLUTION ------------------------------------*/

	//	System.out.println ("Solution");
		aux_colors = 0;
		if (unfeas == 0) {
			for (int i = 0; i < n_nodes; i++ ) {
				if (aux_colors < nodes[i].color) {
					aux_colors = nodes[i].color;
				}
		//		System.out.println (solution[i]);
			}
			if (aux_colors < final_colors ) {
				final_colors = aux_colors;
				System.out.println ("New Best: " + final_colors);
				for (int i = 0; i < n_nodes; i++ ) {
					solution[i] = nodes[i].color;
		//			System.out.println (solution[i]);
				}
				unsucces = 0;
				break;	/* If we were able to improve the number of colors, then we try less colors
					If we were not, the program will end */
			}
		}
	}

}
/*		for (int i = 0; i < n_nodes; i++ ) {
			System.out.println (solution[i]);
		}
*/




	/*----------------------------- OUTPUT SOLUTION IN A FILE ------------------------------------*/

	FileWriter fichero = null;
        PrintWriter pw = null;
        try {
            fichero = new FileWriter("out");
            pw = new PrintWriter(fichero);
 
            for (int i = 0; i < n_nodes; i++)
                pw.write(solution[i]+ " ");
 
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
           try {
           // Nuevamente aprovechamos el finally para
           // asegurarnos que se cierra el fichero.
           if (null != fichero)
              fichero.close();
           } catch (Exception e2) {
              e2.printStackTrace();
           }
        }





	}
}


