all: tsp

tsp.o: tsp.c
	gcc -c tsp.c -Wall

funciones.o: funciones.c
	gcc -c funciones.c -Wall

tsp_funciones.o: tsp_funciones.c
	gcc -c tsp_funciones.c -Wall -lm

tsp: tsp.o funciones.o tsp_funciones.o funciones.h tsp_funciones.h
	gcc -o tsp tsp.o funciones.o  tsp_funciones.o -Wall -lm

