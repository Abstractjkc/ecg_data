#include <stdio.h>
#include <stdlib.h>
#define TRAINNUM (64535)
#define PNUM (300)
void loadData(const char* filename, int row, int col, double **input, int *label);

int main() {
	double** input;
	int *label = (int*)malloc(TRAINNUM*sizeof(int));
	input = (double **)malloc(TRAINNUM * sizeof(double*));
	for (int i = 0; i < TRAINNUM; ++i) {
		input[i] = (double*)malloc(PNUM * sizeof(double));
	}
	loadData("traindata.txt", TRAINNUM, PNUM, input, label);
	for (int i = 0; i < 10; ++i) {
		printf("%d\n", label[i]);
	}
	for (int i = 0; i < TRAINNUM; ++i) free(input[i]);
	free(input);
	free(label);
	return 0;
}

void loadData(const char* filename, int row, int col, double **input, int *label) {
	if (input == NULL || label == NULL) return;
	FILE *df = fopen(filename, "r");
	for (int i = 0; i < row; ++i) {
//		printf("Reading No.%d data...\n", i + 1);
		for (int j = 0; j < col; ++j) {
			fscanf(df, "%lf", &input[i][j]);
		}
		fscanf(df, "%d", &label[i]);
	}
	fclose(df);
}
