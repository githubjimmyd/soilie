#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <opencv\cxcore.h>
#include <opencv\cv.h>
#include <opencv\highgui.h>
#include "cloning.h"

using namespace std;
using namespace cv;


int main(int argc, char** argv)
{
	cloning Clone;
	IplImage *result;
	if(Clone.initialization("source.jpg","background.jpg","source_mask.png", "dest_mask.png"))
	{
		Clone.pasteImage();
		result = Clone.evaluate();
		cvSaveImage("background.jpg", result);
	}
	waitKey(0);
	return 0;
}
