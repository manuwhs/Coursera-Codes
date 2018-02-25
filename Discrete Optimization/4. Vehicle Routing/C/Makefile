all: vrp

vrp.o: vrp.c
	gcc -c vrp.c -Wall

funciones.o: funciones.c
	gcc -c funciones.c -Wall

vrp_funciones.o: vrp_funciones.c
	gcc -c vrp_funciones.c -Wall -lm

vrp: vrp.o funciones.o vrp_funciones.o funciones.h vrp_funciones.h
	gcc -o vrp vrp.o funciones.o  vrp_funciones.o -Wall -lm

