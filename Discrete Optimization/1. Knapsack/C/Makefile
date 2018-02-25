all: knap
knap.o: knap.c
	gcc -c knap.c -Wall

funciones.o: funciones.c
	gcc -c funciones.c -Wall

DP.o: DP.c
	gcc -c DP.c -Wall

BB.o: BB.c
	gcc -c BB.c -Wall

knap: knap.o funciones.o DP.o BBDP.o
	gcc -o knap knap.o funciones.o DP.o BBDP.o -Wall

