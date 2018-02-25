all: graph

clean:
	rm -f *.o
	rm -f *.txt

graph.o: graph.c
	gcc -c graph.c -Wall -lSDL

funciones.o: funciones.c
	gcc -c funciones.c -Wall -lm -lSDL

funciones2.o: funciones2.c
	gcc -c funciones2.c -Wall -lm -lSDL



graph: funciones.o graph.o funciones2.o
	gcc -o graph graph.o funciones.o funciones2.o -Wall -lm -lSDL
