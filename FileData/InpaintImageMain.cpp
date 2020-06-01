#include <opencv2\imgproc\imgproc.hpp>
#include <opencv2/photo/photo.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "InpaintImage.cpp"
#include <iostream>
#include <stdlib.h>
#include "math.h"

#define SRC		"background.jpg"
#define MASK	"background_mask.jpg"
#define BASE_RADIUS	4

using namespace std;
using namespace cv;

int main()
{
	Inpaint Inpt;
	cv::Mat srcimg = cv::imread(SRC,CV_LOAD_IMAGE_COLOR);
	cv::Mat maskimg = cv::imread(MASK,CV_LOAD_IMAGE_GRAYSCALE);
	int width = srcimg.cols;
	int height = srcimg.rows;

	// get mask pixels
	BYTE *maskpx = new BYTE[maskimg.cols*maskimg.rows];
	for(int i=0; i<maskimg.cols;i++)
	{
		for(int j=0; j<maskimg.rows; j++)
		{
			if(maskimg.at<uchar>(j,i)!=0)
				maskimg.at<uchar>(j,i) = 255;
			maskpx[j*maskimg.cols+i] = maskimg.at<uchar>(j,i);
		}
	}

	// get source pixels
	float *srcpx = new float[width*height*3];
	for(int j=0; j<height; j++)
	{
		for(int i=0; i<width; i++)
		{
			for(int k=0;k<3;k++)
				srcpx[(j*width+i)*3+k] = srcimg.at<Vec3b>(j,i)[k];
		}
	}

	//inpaint image
	if(!Inpt.Inpainting(srcpx, maskpx, width, height, BASE_RADIUS))
		return 0;

	//save as a new image
	cv::Mat inptimg = cv::imread(SRC,CV_LOAD_IMAGE_COLOR);
	for(int j=0; j<inptimg.rows;j++)
	{
		for(int i=0; i<inptimg.cols; i++)
		{
			for(int k=0; k<3;k++)
				inptimg.at<Vec3b>(j,i)[k] = srcpx[(j*width+i)*3+k];
		}
	}
	imwrite("background.jpg",inptimg);

	waitKey(0);
	return 0;
}
