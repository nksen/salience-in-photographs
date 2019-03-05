#include <iostream>
#include "StopWatch.h"
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace std;
using namespace cv;

StopWatch timer;

/*
// returns a matrix of the cumulative sum of the input matrix. eg:
1 2 3	 1  3  6
4 5 6 -> 5  12 21
7 8 9	 12 27 45
// matrix is 1D array where coords (i, j) are at [i * cols + j]
// the number of rows and columns in the matrix is rows and columns
*/
unsigned int* cumsum(unsigned int* matrix, unsigned int* sum, unsigned int rows, unsigned int cols) {

	// row/col zero are done sepertaely to avoid a negative index
	sum[0] = matrix[0];

	for (int j = 1; j < cols; j++) {
		sum[j] = sum[j - 1] + matrix[j];
	}

	// total keeps track of the cumulative sum of the row
	unsigned int row_sum;

	// loop over matrix
	for (int i = 1; i < rows; i++) {

		// reset total at each new row
		row_sum = 0;

		for (int j = 0; j < cols; j++) {

			// update row and overal cumulative sum 
			row_sum += matrix[i * cols + j];
			sum[i * cols + j] = sum[(i - 1) * cols + j] + row_sum;

		}
	}

	return sum;
}

void cumsum(uchar* matrix, unsigned long* sum, size_t rows, size_t cols) {

	// row/col zero are done sepertaely to avoid a negative index
	sum[0] = matrix[0];

	for (size_t j = 1; j < cols; ++j) {
		sum[j] = sum[j - 1] + matrix[j];
	}

	// total keeps track of the cumulative sum of the row
	// TODO Overflow
	unsigned int row_sum;

	// loop over matrix
	for (size_t i = 1; i < rows; ++i) {

		// reset total at each new row
		row_sum = 0;

		for (int j = 0; j < cols; j++) {

			// update row and overal cumulative sum 
			row_sum += matrix[i * cols + j];
			sum[i * cols + j] = sum[(i - 1) * cols + j] + row_sum;

		}
	}
}

inline double cost(unsigned int* sum, unsigned int i, unsigned int j, unsigned int cols) {
	return sum[i * cols + j] / (i * i * j * j);
}


int main() {

	Mat image;
	image = imread("bird.jpeg", CV_LOAD_IMAGE_GRAYSCALE);   // Read the file

	if (!image.data)                              // Check for invalid input
	{
		cout << "Could not open or find the image" << std::endl;
		return -1;
	}


	size_t rows = image.size.p[0];
	size_t cols = image.size.p[1];

	unsigned long* sum = new unsigned long[rows * cols];

	cumsum(&image.data[0], sum, rows, cols);

	cout << int(sum[rows * cols - 1]);

	namedWindow("Display window", WINDOW_AUTOSIZE);// Create a window for display.
	imshow("Display window", image);                   // Show our image inside it.

	waitKey(0);                                          // Wait for a keystroke in the window
	
	
	delete[] sum;
	
	return 0;

}
