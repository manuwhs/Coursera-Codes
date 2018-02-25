#include <stdio.h>
#include <stdlib.h>
#include <SDL/SDL.h>
#include "funciones.h"

int main(int argc, char *argv[]) {
	SDL_Surface *image, *screen;	/* Supercifies a mostrar */
	SDL_Rect dest;
	SDL_Event event;
	int i,j ;
	int done = 0;
	int scX = 900, scY = 700;

	FILE *pf;
	char cad[200] = "./plot/in";
	int nodeCount;
	float * eje_X;
	float * eje_Y;
	int * order;

	float max_X;
	float max_Y;

	pf = fopen(cad, "r+");
	if (pf == NULL) {
		perror ("Error al abrir el archivo");
	}
	fscanf (pf, "%d",&nodeCount);
	printf("Mira %i \n",nodeCount);

	eje_X = (float * )malloc(nodeCount*sizeof(float));
	eje_Y = (float * )malloc(nodeCount*sizeof(float));
	order = (int * )malloc(nodeCount*sizeof(int));

	for (i = 0; i < nodeCount; i++) {
		fscanf(pf, "%f",eje_X + i);
		fscanf(pf, "%f",eje_Y + i);
//		printf(" Nodo %i: (%f,%f) \n",i,eje_X[i],eje_Y[i]);
	}

	fclose(pf);

	pf = fopen("./plot/out", "r+");
		
	for (i = 0; i < nodeCount; i++) {
		fscanf(pf, "%d",order + i);
//		printf(" %i ", order[i]);
	}

	fclose(pf);

	max_X = maxf(eje_X,nodeCount);
	max_Y = maxf(eje_Y,nodeCount);

	/* Normalizamos los puntos para representarlos */
	for (i = 0; i < nodeCount; i++) {
		eje_X[i] = eje_X[i]*(scX - 50)/max_X;
		eje_Y[i] = eje_Y[i]*(scY - 50)/max_Y;
//		printf(" Nodo %i: (%f,%f) \n",i,eje_X[i],eje_Y[i]);
	}

	atexit(SDL_Quit);	/* A la salida desinicializamos todo */
	// Iniciar SDL y joystick
	if (SDL_Init(SDL_INIT_VIDEO| SDL_INIT_JOYSTICK ) < 0) {
		printf("No se pudo iniciar SDL: %s\n",SDL_GetError());
		exit(1);
	}

	// Activamos modo de video
	screen = SDL_SetVideoMode(scX,scY,24,SDL_HWSURFACE);
	if (screen == NULL) {
		printf("No se puede inicializar el modo gráfico: \n");
		exit(1);
	} 

//	SDL_BlitSurface(image, NULL, screen, &dest);	/* Colocamos la imagen en la pantalla */

	// rectangle (screen, 300,200,100,250, 0x22222222);
	// line (screen, 300,200,600,400,10, 0x22222222);

	for (i = 0; i < nodeCount; i++) {
//		printf(" Nodo %i dibujao \n",i);
		
		circle (screen, (int)eje_X[i] + 15,(int) eje_Y[i] + 15 ,4, 0x88888800);
	}

line (screen, (int)eje_X[order[0]]+15, (int)eje_Y[order[0]]+ 15,(int)eje_X[order[nodeCount-1]]+ 15, (int)eje_Y[order[nodeCount-1]]+ 15 ,1, 0xffffffff);
SDL_Flip(screen);
	for (i = 0; i < nodeCount-1; i++) {
// printf(" Puntos: (%i,%i) -> (%i,%i) \n",(int)eje_X[order[i]], (int)eje_Y[order[i]],(int)eje_X[order[i+1]], (int)eje_Y[order[i+1]]);
line (screen, (int)eje_X[order[i]]+ 15, (int)eje_Y[order[i]]+ 15,(int)eje_X[order[i+1]]+ 15, (int)eje_Y[order[i+1]]+ 15 ,2,0xffffffff);
//	rectangle (screen, (int)eje_X[order[i]]-5,(int)eje_Y[order[i]]-5,10,10, 0xffffffff);
//	cad[0] = getchar(); 

	}
SDL_Flip(screen);
		// Mostramos la pantalla
	SDL_Flip(screen);	/* Utilizado para refrescar la pantalla tambien */



	// Esperamos la pulsación de una tecla para salir
	while(done == 0) {
		while ( SDL_PollEvent(&event) ) {
			if ( event.type == SDL_KEYDOWN )
				done = 1;
			}
		}


	/* Liberamos y salimos */

	SDL_FreeSurface(screen);
	SDL_Quit();
	free(eje_X);
	free(eje_Y);
	free(order);
	printf("\nTodo ha salido bien.\n");
	return 0;
}




