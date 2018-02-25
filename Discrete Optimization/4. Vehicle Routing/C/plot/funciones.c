#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <SDL/SDL.h>

/* FUNCIONES PARA GRAFICOS */

void putpixel(SDL_Surface *surface, int x, int y, Uint32 pixel) {

	int bpp = surface->format->BytesPerPixel;
	/* Here p is the address to the pixel we want to set */
	Uint8 *p = (Uint8 *)surface->pixels + y * surface->pitch + x * bpp;
	switch(bpp) {
		case 1:
			*p = pixel;
			break;
		case 2:
			*(Uint16 *)p = pixel;
			break;
		case 3:
			if(SDL_BYTEORDER == SDL_BIG_ENDIAN) {
				p[0] = (pixel >> 16) & 0xff;
				p[1] = (pixel >> 8) & 0xff;
				p[2] = pixel & 0xff;
			} 
			else {
				p[0] = pixel & 0xff;
				p[1] = (pixel >> 8) & 0xff;
				p[2] = (pixel >> 16) & 0xff;
			}
			break;
		case 4:
			*(Uint32 *)p = pixel;
			break;
	}
}


void rectangle (SDL_Surface *surface, int x, int y, int w, int h, Uint32 pixel) {
	int i,j;
	for (i = 0; i < w; i++) {
		for (j = 0; j < h; j++) {
			putpixel(surface, x + i , y + j, pixel);
		}
	}
}

void line (SDL_Surface *surface, int x1, int y1, int x2, int y2, int t, Uint32 pixel) {
	int i,j;
	int slope = 0; 
	int slope2 = 0;
	int aux;
	
	int dx = 1;
	int dy = 1;



	if ((x2 - x1 != 0)&&(y2 - y1 != 0)) {
		 slope =1000* (y2 - y1) / (x2 - x1);
		 slope2 =1000* (x2 - x1) / (y2 - y1);
	


		if (abs(slope)<= 1000) {
			if (x1 > x2) {
				dx = -1;
			}

			for (i = 0; i < abs(x2 - x1); i++) {
				for (j = 0; j < t; j++) {	/* Grosor */
// As this goes from left to right:

					putpixel(surface, x1 + dx*i + j -t/2, y1 + dx*i*slope/1000, pixel);
				}
			}
		}
		else {
			for (i = 0; i < abs(y2 - y1); i++) {

			if (y1 > y2) {
				dy = -1;
			}
				for (j = 0; j < t; j++) {	/* Grosor */

					putpixel(surface, x1 + dy*i*slope2/1000 ,y1 + dy*i + j -t/2 , pixel);


				}
			}
		}

	}

	else if (x2 - x1 == 0){
		for (i = 0; i < abs(y2 - y1); i++) {

			if (y1 > y2) {
				dy = -1;
			}
			for (j = 0; j < t; j++) {	/* Grosor */

				putpixel(surface, x1 + dy*i*slope2/1000 ,y1 + dy*i + j -t/2 , pixel);


			}
		}
	}

	else if (y2 - y1 == 0){
			if (x1 > x2) {
				dx = -1;
			}

			for (i = 0; i < abs(x2 - x1); i++) {
				for (j = 0; j < t; j++) {	/* Grosor */
// As this goes from left to right:

					putpixel(surface, x1 + dx*i + j -t/2, y1 + dx*i*slope/1000, pixel);
				}
			}
	}

}

void line2 (SDL_Surface *surface, int x1, int y1, int x2, int y2, int t, Uint32 pixel) {
	int i,j;
	int slope = 100; 
	int slope2 = 100;

			for (i = 0; i < y2 - y1; i++) {
				for (j = 0; j < t; j++) {	/* Grosor */
					putpixel(surface, x1 + i ,y1 + i + j -t/2 , pixel);
				}
			}


}

void circle (SDL_Surface *surface, int x, int y, int r, Uint32 pixel) {
	int i,j;
	int y_pos;

	for (i = 0; i < r+1; i++) {
		y_pos = 1000 * sqrt(r*r - ((i-r)*(i-r)) );

		for (j = 0; j < y_pos/1000 + 1; j++) {
			putpixel(surface, x + i - r, y + j, pixel);
			putpixel(surface, x + i - r, y - j, pixel);

			putpixel(surface, x + r - i, y + j, pixel);
			putpixel(surface, x + r - i, y - j, pixel);
		}
	}
}

void triangle (SDL_Surface *surface, int x1, int y1, int x2, int y2, int x3, int y3, Uint32 pixel) {
	line (surface, x1,y1,x2,y2,100, pixel);
	line (surface, x1,y1,x3,y3,100, pixel);
	line (surface, x2,y2,x3,y3,100, pixel);
}

/* FUNCIONES PARA LEER ARCHIVOS */



