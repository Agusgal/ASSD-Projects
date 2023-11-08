/*
Archivo principal por el cual se realizan las pruebas de las funciones utilizadas y donde luego se verá
la comparación entre la FFT en su totalidad contra la de mathlab y phython
*/

//Librerias
#include "FFT.h"

//Main
int main()
{
	//Variables para testear
	vector<complex<float>> in = { 5,8,10,3,5,6,2,0,0,1,2,3,4,5,6,7,8,9,10,11,4,4,5,6,7,1,1,2,2,4,5,2 };
	vector<complex<float>> out = { 52, 78 };
	size_t N = in.size();
	//Testeo
	cout << "FFT input:" << endl;
	for (unsigned int i = 0; i < N; i++) {
		cout << in[i] << endl;
	}
	fft(in, out, N);
	cout << "FFT output:" << endl;
	for (unsigned int i = 0; i < N; i++) {
		cout << out[i] << endl;
	}
}