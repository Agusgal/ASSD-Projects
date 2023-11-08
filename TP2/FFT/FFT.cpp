/*
Función que realiza la FFT de un arreglo de hasta 4096 puntos por medio de la implementación del algoritmo de 
Cooley-Tukey. 
La funcion espera por lo menos se le envie el in y out, en caso de no enviarselos o envierle algo erroneo por
el mismo su comportamiento va a ser erratico y no definido.
El algoritmo se aplico utilizando las muestras ordenadas tal como vinieron causando que la salida se encuentre
con sus bits de posiciones invertidas
*/

#include "FFT.h"

void fft(vector<complex<float>>& in, vector<complex<float>>& out,size_t n) {
	//Variables Temporales
	complex<float> A, B,TEMP;
	size_t REVERSBIT;
	//Asumiendo que no se envia el n lo busco
	size_t N = in.size();
	
	//En caso de haberlo recibido
	if (n != 0) {
		N = n;
	}

	//Chequeo si el numero es 1
	if (N == 1) {
		out[0] = in[0];
		return;
	}
	//Si no es  potencia de 2 lo vuelvo potencia de 2 agregando ceros al final del arreglo
	else if ( ( (fmod(log2(N), 1)) != 0 ) && (N <= 4096) )
	{
		while ( (fmod(log2(N), 1)) != 0 )
		{
			in.insert(in.end(), (complex<float>)0);
			N = in.size();
		}
	}
	//En casoque el numero supere los 4096 solo utilizamos los primeros 40936 datos
	else if (N >= 4096) {
		N = 4096;
	}
	//En caso de ser potencia de 2 no hacemos nada

	// Calculo el numero de etapas del argoritmo que es cada subdivisión en grupos realizada
	size_t ETAPAS = (size_t)log2(N);
	// Inicializo cantidad de grupor por etapa
	size_t GRUPOS = 1;
	// Inicializo cantidad de mariposas (Suma de muestras y multiplicación de Wn )
	size_t MARIPOSAS = N / 2;
	//Inicializo la salida en caso de que sea diferente a la entrada
	if ((&in) != (&out)) {
		out = in;
	}

	//Algoritmo
	for (size_t e = 0; e < ETAPAS; e++){
		for (size_t g = 0; g < GRUPOS; g++){
			for (size_t m = 0; m < MARIPOSAS; m++)
			{
				A = out[m + 2 * MARIPOSAS * g];
				B = out[m + 2 * MARIPOSAS * g + ((size_t)(N / pow(2, e + 1)))] * Wn[g];
				out[m + 2 * MARIPOSAS * g] = A + B;
				out[m + 2 * MARIPOSAS * g + ((size_t)(N / pow(2, e + 1)))] = A - B;
			}
		}
		GRUPOS *= 2;
		MARIPOSAS /= 2;
	}

	//Por ultimo se acomada el arreglo
	for (size_t i = 0; i < N; i++)
	{
		REVERSBIT = bit_rev(i, ETAPAS);
		//Evito repetir intercambios
		if (i < REVERSBIT) {
			TEMP = out[i];
			out[i] = out[REVERSBIT];
			out[REVERSBIT] = TEMP;
		}
	}
}


//Funcion de inversión de bits
size_t bit_rev(size_t num, size_t nbits) {
	size_t rnum = num;	//Numero a invertir
	switch (nbits) {
	case 0:
		rnum = 0;
	case 1:
		rnum = BR1[num];
		break;
	case 2:
		rnum = BR2[num];
		break;
	case 3:
		rnum = BR3[num];
		break;
	case 4:
		rnum = BR4[num];
		break;
	case 5:
		rnum = BR5[num];
		break;
	case 6:
		rnum = BR6[num];
		break;
	case 7:
		rnum = BR7[num];
		break;
	case 8:
		rnum = BR8[num];
		break;
	case 9:
		rnum = BR9[num];
		break;
	case 10:
		rnum = BR10[num];
		break;
	case 11:
		rnum = BR11[num];
		break;
	case 12:
		rnum = BR12[num];
		break;
	default:
		printf("Error: El número de bits ingresado es incorrecto");
		break;
	}
	return rnum;
}

// Ejecutar programa: Ctrl + F5 o menú Depurar > Iniciar sin depurar
// Depurar programa: F5 o menú Depurar > Iniciar depuración

// Sugerencias para primeros pasos: 1. Use la ventana del Explorador de soluciones para agregar y administrar archivos
//   2. Use la ventana de Team Explorer para conectar con el control de código fuente
//   3. Use la ventana de salida para ver la salida de compilación y otros mensajes
//   4. Use la ventana Lista de errores para ver los errores
//   5. Vaya a Proyecto > Agregar nuevo elemento para crear nuevos archivos de código, o a Proyecto > Agregar elemento existente para agregar archivos de código existentes al proyecto
//   6. En el futuro, para volver a abrir este proyecto, vaya a Archivo > Abrir > Proyecto y seleccione el archivo .sln
