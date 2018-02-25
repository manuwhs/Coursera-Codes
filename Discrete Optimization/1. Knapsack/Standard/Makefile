all: knap
knap.o: knap.c
	gcc -c knap.c -Wall -fno-stack-protector 

funciones.o: funciones.c
	gcc -c funciones.c -Wall -fno-stack-protector 

DP.o: DP.c
	gcc -c DP.c -Wall -fno-stack-protector 

BB.o: BB.c
	gcc -c BB.c -Wall -fno-stack-protector 

knap: knap.o funciones.o DP.o BB.o
	gcc -o knap knap.o funciones.o DP.o BB.o -Wall -fno-stack-protector 

