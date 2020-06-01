//#include <opencv2\imgproc\imgproc.hpp>
//#include <opencv2/photo/photo.hpp>
//#include <opencv2/highgui/highgui.hpp>
//#include <opencv2/core/core.hpp>
//#include "inpaint.h"
//#include <iostream>
//#include <stdlib.h>
//
//using namespace std;
//using namespace cv;
//
//int main()
//{
//	cv::Mat img = cv::imread("background.jpg",CV_LOAD_IMAGE_COLOR);
//	cv::Mat impaintMask = cv::imread("background_mask.jpg",CV_LOAD_IMAGE_GRAYSCALE);
//	cv::Mat inpainted;
//	Inpaint inPaintImg;
//	cv::inpaint(img,impaintMask,inpainted,3,INPAINT_TELEA);
//
//	namedWindow("inpaint", WINDOW_AUTOSIZE);
//	imshow("inpaint", inpainted);
//	imwrite("inpainted.png",inpainted);
//	waitKey(0);
//	return 0;
//
//}