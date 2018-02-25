all: decryp1

clean:

	rm -f *.o
	rm -f practica2_malloc
	rm -f practica2_mmap
	rm -f *.txt

OTP.o: OTP.c
	gcc -c OTP.c -Wall

OTP1.o: OTP1.c
	gcc -c OTP1.c -Wall

OTP3.o: OTP3.c
	gcc -c OTP3.c -Wall

funciones.o: funciones.c
	gcc -c funciones.c -Wall

pruebas.o: pruebas.c
	gcc -c pruebas.c -Wall

problem.o: problem.c
	gcc -c problem.c -Wall

pruebas: funciones.o pruebas.o
	gcc -o pruebas pruebas.o funciones.o -Wall

decryp: funciones.o OTP.o
	gcc -o decryp OTP.o funciones.o -Wall

decryp1: funciones.o OTP1.o
	gcc -o decryp1 OTP1.o funciones.o -Wall

decryp3: funciones.o OTP3.o
	gcc -o decryp3 OTP3.o funciones.o -Wall

problem: funciones.o problem.o
	gcc -o problem problem.o funciones.o -Wall
