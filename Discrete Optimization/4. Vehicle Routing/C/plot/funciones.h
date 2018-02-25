#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <SDL/SDL.h>

void zero_char (char * array, int length); 
void zero_int (int * array, int length); 
int str2dec(char  * cad, char digit); 

float str2float(char  * cad, char digit);

void get_items (char * data, int * capacity, int * items, int ** weights, int ** values); 
char * obtener_datos(char * archivo); 

void get_points (char * archivo, int * n_nodes, float ** points);

int max(int a, int b);
float maxf (float * array, int num);

int findint(int * array, int len, int value);
int dec2str(char  * cad, int digit);
int copy_vector_char(char * duplicado, char * original, int num);
int count_char(char * array, int len, int value);
int ordenar_int (int * lista, int * orden, int len);
int copy_vector_int(int * duplicado, int * original, int num);
int reordenar_int (int * lista, int * orden, int len);
int desreordenar_char (char * lista, int * orden, int len); 

void putpixel(SDL_Surface *surface, int x, int y, Uint32 pixel);
void rectangle (SDL_Surface *surface, int x, int y, int w, int h, Uint32 pixel);
void line (SDL_Surface *surface, int x1, int y1, int x2, int y2, int t, Uint32 pixel);
void circle (SDL_Surface *surface, int x, int y, int r, Uint32 pixel);
