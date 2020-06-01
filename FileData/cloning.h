#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <opencv\cxcore.h> 
#include <opencv\cv.h>
#include <opencv\highgui.h>
#include "math.h"

using namespace std;
using namespace cv;

#define pi 3.1416

class cloning{
public:
	IplImage *src, *dest, *srcmsk, *dstmsk, *roiDst;
	RECT roi_src;
	int roix, roiy;
	int dstx, dsty;


	
//---------------------------------------------------------
// Initialize the source and destination images and masks
//---------------------------------------------------------
bool initialization(char* source, char* destination, char* srcmask, char* dstmask)
{
	src = cvLoadImage(source);
	dest = cvLoadImage(destination);
	srcmsk = cvLoadImage(srcmask);
	dstmsk = cvLoadImage(dstmask);
	if(src!=NULL && dest!=NULL && srcmsk!=NULL && dstmsk!=NULL)
	{	
		findRoi();
		findDestinationPoint();
		return true;
	}
	return false;
};

//---------------------------------------------------------
// Find the ROI from source's mask
//---------------------------------------------------------
void findRoi()
{
	roi_src.right = roi_src.bottom = 0;
	roi_src.left = src->width;
	roi_src.top = src->height;
	for(int j=0; j<srcmsk->height; j++)
	{
		for(int i=0; i<srcmsk->width; i++)
		{
			double r = cvGet2D(srcmsk,j,i).val[2];
			double g = cvGet2D(srcmsk,j,i).val[1];
			double b = cvGet2D(srcmsk,j,i).val[0];
			if(r==255 && g==255 && b==255)
			{
				if(roi_src.left>i)
					roi_src.left = i;
				if(roi_src.right<i)
					roi_src.right = i;
				if(roi_src.top>j)
					roi_src.top = j;
				if(roi_src.bottom<j)
					roi_src.bottom = j;
			}
		}
	}
};


//---------------------------------------------------------
// Find the paste point from destination's mask
//---------------------------------------------------------
void findDestinationPoint()
{
	bool found_dstpoint = false;
	for(int j=0; j<dstmsk->height; j++)
	{
		for(int i=0; i<dstmsk->width; i++)
		{
			double r = cvGet2D(dstmsk,j,i).val[2];
			double g = cvGet2D(dstmsk,j,i).val[1];
			double b = cvGet2D(dstmsk,j,i).val[0];
			if(!found_dstpoint && r==255 && g==0 && b==0)
			{
				//find the place to paste
				found_dstpoint = true;
				dstx = i;
				dsty = j;
			}
		}
	}
	if(!found_dstpoint)
	{
		MessageBox(0,"Cannot find the destination point in the 'dest_mask', maybe it is not in color RED(255,0,0)?",
			"Cannot Find Destination Point",0);
		exit(0);
	}
};

//------------------------------------------------------------
// Paste ROI image from source to an empty destination image
//------------------------------------------------------------
void pasteImage()
{
	roiDst = cvCreateImage(cvGetSize(dest),dest->depth, dest->nChannels);
	cvZero(roiDst);

	for(int i=roi_src.left, ix=0; i<=roi_src.right; i++, ix++)
	{
		for(int j=roi_src.top, jy=0; j<=roi_src.bottom; j++, jy++)
		{
			// get source mask color at this point
			int mr = cvGet2D(srcmsk, j, i).val[2];
			int mg = cvGet2D(srcmsk, j, i).val[1];
			int mb = cvGet2D(srcmsk, j, i).val[0];
			if(mr==255 && mg==255 && mb==255)
			{
				// get source color at this point
				int sr = cvGet2D(src, j, i).val[2];
				int sg = cvGet2D(src, j, i).val[1];
				int sb = cvGet2D(src, j, i).val[0];
				CvScalar bgr = cvScalar(sb, sg, sr);
				// roiDst is an image with roi image pasted to the destination point
				if(dsty+jy<roiDst->height && dstx+ix<roiDst->width)
					cvSet2D(roiDst,dsty+jy,dstx+ix, bgr);
			}
		}
	}
};


//-----------------------------------------------------------
// clone and get the result
//-----------------------------------------------------------
IplImage *evaluate()
{
    IplImage *gradientx  = cvCreateImage(cvGetSize(dest), 32, 3);
    IplImage *gradienty  = cvCreateImage(cvGetSize(dest), 32, 3);

    IplImage *roiDst_gradx  = cvCreateImage(cvGetSize(roiDst), 32, 3);
    IplImage *roiDst_grady  = cvCreateImage(cvGetSize(roiDst), 32, 3);

    IplImage *whitemap   = cvCreateImage(cvGetSize(dest), 8, 3);
    IplImage *erowhmp  = cvCreateImage(cvGetSize(dest), 8, 3);
    IplImage *refdest  = cvCreateImage(cvGetSize(dest), 8, 3);

    cvZero(whitemap);
    cvZero(refdest);

    IplImage *O    = cvCreateImage(cvGetSize(dest), 8, 3);
    IplImage *error= cvCreateImage(cvGetSize(dest), 8, 3);

    int w = dest->width;
    int h = dest->height;
    int channel = dest->nChannels;

    int roiw = roi_src.right-roi_src.left;
    int roih = roi_src.bottom-roi_src.top;

	//get gradiant from destination image and roiDst mask
    getGradientx(dest,gradientx);
    getGradienty(dest,gradienty);

    getGradientx(roiDst,roiDst_gradx);
    getGradienty(roiDst,roiDst_grady);

	//copy the white roi from source mask to a new empty destination map (whitemap)
	for(int j=dsty, jj=roi_src.top; j<dsty+roih; j++,jj++)
	{
		for(int i=dstx, ii=roi_src.left; i<dstx+roiw; i++,ii++)
		{
			int mr = cvGet2D(srcmsk, jj, ii).val[2];
			int mg = cvGet2D(srcmsk, jj, ii).val[1];
			int mb = cvGet2D(srcmsk, jj, ii).val[0];
			if(mr==255 && mg==255 && mb==255)
			{
				for(int c=0;c<channel;++c)
				{
					((uchar*)(whitemap->imageData + whitemap->widthStep*j))[i*channel+c] = 255;
				}
			}
		}
	}

    cvErode(whitemap,erowhmp);

    IplImage* whmp_mask = cvCreateImage(cvGetSize(erowhmp),32,3);
	IplImage* maskGradientx = cvCreateImage(cvGetSize(refdest),32,3);
	IplImage* maskGradienty = cvCreateImage(cvGetSize(refdest),32,3);

    cvConvertScale(erowhmp,whmp_mask,1.0/255.0,0.0);
    cvConvertScale(dest,maskGradientx,1.0/255.0,0.0);
    cvConvertScale(dest,maskGradienty,1.0/255.0,0.0);

	// get mask's gradient
    for(int i=0;i < h; i++)
	{
        for(int j=0; j < w; j++)
		{
            for(int c=0;c<channel;++c)
            {
				//get product of array sgx and smask, and product of sgy and smask
				((float*)(maskGradientx->imageData + maskGradientx->widthStep*i))[j*channel+c] =
					((float*)(roiDst_gradx->imageData + roiDst_gradx->widthStep*i))[j*channel+c] *
					((float*)(whmp_mask->imageData + whmp_mask->widthStep*i))[j*channel+c];

				((float*)(maskGradienty->imageData + maskGradienty->widthStep*i))[j*channel+c] =
					((float*)(roiDst_grady->imageData + roiDst_grady->widthStep*i))[j*channel+c] *
					((float*)(whmp_mask->imageData + whmp_mask->widthStep*i))[j*channel+c];
            }
		}
	}

    cvNot(erowhmp,erowhmp);

	whmp_mask = cvCreateImage(cvGetSize(erowhmp),32,3);
	IplImage* destGradientx = cvCreateImage(cvGetSize(refdest),32,3);
	IplImage* destGradienty = cvCreateImage(cvGetSize(refdest),32,3);

    cvConvertScale(erowhmp,whmp_mask,1.0/255.0,0.0);
	cvConvertScale(dest,destGradientx,1.0/255.0,0.0); 
    cvConvertScale(dest,destGradienty,1.0/255.0,0.0);

	// get get product of array grx and smask1, and the product of gry and smask1
    for(int i=0;i < h; i++)
	{
        for(int j=0; j < w; j++)
		{
            for(int c=0;c<channel;++c)
            {
				((float*)(destGradientx->imageData + destGradientx->widthStep*i))[j*channel+c] =
					((float*)(gradientx->imageData + gradientx->widthStep*i))[j*channel+c] *
					((float*)(whmp_mask->imageData + whmp_mask->widthStep*i))[j*channel+c];

				((float*)(destGradienty->imageData + destGradienty->widthStep*i))[j*channel+c] =
					((float*)(gradienty->imageData + gradienty->widthStep*i))[j*channel+c] *
					((float*)(whmp_mask->imageData + whmp_mask->widthStep*i))[j*channel+c];
            }
		}
	}
	IplImage *final = cvCreateImage(cvGetSize(dest), 8, 3 );
	poisson(destGradientx,destGradienty,maskGradientx,maskGradienty,final);
	return final;
};



//----------------------------------------------------------------------
// Use the Laplacian ooperator and the Poisson equation to blend images
//----------------------------------------------------------------------
void poisson(IplImage* destGradientx,IplImage* destGradienty,IplImage* maskGradientx,IplImage* maskGradienty,IplImage* final)
{
	IplImage *gx  = cvCreateImage(cvGetSize(dest), 32, 3);
    IplImage *gy  = cvCreateImage(cvGetSize(dest), 32, 3);
	IplImage *refdest  = cvCreateImage(cvGetSize(dest), 8, 3);
	cvZero(refdest);
	IplImage* fx = cvCreateImage(cvGetSize(refdest),32,3);
    IplImage* fy = cvCreateImage(cvGetSize(refdest),32,3);

	int w = dest->width;
    int h = dest->height;
    int channel = dest->nChannels;

	//add the destination image's gradient and the mask's gradient
    for(int j=0; j < h; j++)
	{
        for(int i=0; i < w; i++)
		{
            for(int c=0;c<channel;++c)
            {
				((float*)(fx->imageData + fx->widthStep*j))[i*channel+c] =
					((float*)(destGradientx->imageData + destGradientx->widthStep*j))[i*channel+c] +
					((float*)(maskGradientx->imageData + maskGradientx->widthStep*j))[i*channel+c];

				((float*)(fy->imageData + fy->widthStep*j))[i*channel+c] =
					((float*)(destGradienty->imageData + destGradienty->widthStep*j))[i*channel+c] +
					((float*)(maskGradienty->imageData + maskGradienty->widthStep*j))[i*channel+c];
			}
		}
	}

    lap(fx,gx,fy,gy);

    IplImage *rgb_rx = cvCreateImage(cvGetSize(dest), 32, 1 );
    IplImage *rgb_gx = cvCreateImage(cvGetSize(dest), 32, 1 );
    IplImage *rgb_bx = cvCreateImage(cvGetSize(dest), 32, 1 );

    cvSplit(gx, rgb_rx, rgb_gx, rgb_bx,0);

    IplImage *rgb_ry = cvCreateImage(cvGetSize(dest), 32, 1 );
    IplImage *rgb_gy = cvCreateImage(cvGetSize(dest), 32, 1 );
    IplImage *rgb_by = cvCreateImage(cvGetSize(dest), 32, 1 );

    cvSplit(gy, rgb_ry, rgb_gy, rgb_by,0);
        
    IplImage *rgb_r = cvCreateImage(cvGetSize(dest), 8, 1 );
    IplImage *rgb_g = cvCreateImage(cvGetSize(dest), 8, 1 );
    IplImage *rgb_b = cvCreateImage(cvGetSize(dest), 8, 1 );

    cvSplit(dest, rgb_r, rgb_g, rgb_b,0);

    Mat output_r = Mat(h,w,CV_8UC1);
    Mat output_g = Mat(h,w,CV_8UC1);
    Mat output_b = Mat(h,w,CV_8UC1);

    poisson_solver(rgb_r,rgb_rx,rgb_ry,output_r);
    poisson_solver(rgb_g,rgb_gx,rgb_gy,output_g);
    poisson_solver(rgb_b,rgb_bx,rgb_by,output_b);
        
    for(int i=0;i<h;i++)
	{
        for(int j=0;j<w;j++)
		{
			((uchar*)(final->imageData + final->widthStep*i))[j*channel+0] = output_r.at<uchar>(i,j);
			((uchar*)(final->imageData + final->widthStep*i))[j*channel+1] = output_g.at<uchar>(i,j);
			((uchar*)(final->imageData + final->widthStep*i))[j*channel+2] = output_b.at<uchar>(i,j);
        }
	}
};

void poisson_solver(const IplImage *img, IplImage *gx , IplImage *gy, Mat &output)
{

    int w = img->width;
    int h = img->height;
    int channel = img->nChannels;

    IplImage *lapp  = cvCreateImage(cvGetSize(img), 32, 1);
    for(int i =0;i<h;i++)
	{
        for(int j=0;j<w;j++)
		{
			((float*)(lapp->imageData + lapp->widthStep*i))[j] =
				((float*)(gy->imageData + gy->widthStep*i))[j] +
				((float*)(gx->imageData + gx->widthStep*i))[j];
		}
	}

    Mat boundary(img);
    for(int i =1;i<h-1;i++)
	{
        for(int j=1;j<w-1;j++)
        {
			boundary.at<uchar>(i,j) = 0;
        }
	}

    // applying the laplacian operator  
    double *boundary_points = new double[h*w];
    for(int i =1;i<h-1;i++)
	{
        for(int j=1;j<w-1;j++)
        {
            boundary_points[i*w+j] = -4*(int)boundary.at<uchar>(i,j) + (int)boundary.at<uchar>(i,(j+1)) + 
				(int)boundary.at<uchar>(i,(j-1)) + (int)boundary.at<uchar>(i-1,j) + (int)boundary.at<uchar>(i+1,j);
        }
	}

    Mat diff = Mat(h,w,CV_32FC1);
    for(int i =0;i<h;i++)
    {
        for(int j=0;j<w;j++)
        {
            diff.at<float>(i,j) = (((float*)(lapp->imageData + lapp->widthStep*i))[j] - boundary_points[i*w+j]);
        }
    }

	delete[] boundary_points; 

    double *temp_diff = new double[(h-2)*(w-2)];
    for(int i = 0 ; i < h-2;i++)
    {
        for(int j = 0 ; j < w-2; j++)
        {
            temp_diff[i*(w-2)+j] = diff.at<float>(i+1,j+1);
        }
    }

    double *m = new double[(h-2)*(w-2)];
	dst(temp_diff,m,h-2,w-2);

	delete[] temp_diff;

    double *m_transp = new double[(h-2)*(w-2)];
    transposition(m,m_transp,h-2,w-2);
    dst(m_transp,m,w-2,h-2);
    transposition(m,m_transp,w-2,h-2);

	double *temp = new double[(h-2)*(w-2)];
    for(int i = 0, cy=1; i < w-2;i++,cy++)
    {
        for(int j = 0,cx = 1; j < h-2; j++,cx++)
        {
            temp[j*(w-2) + i] = (float) 2*cos(pi*cy/( (double) (w-1))) - 2 
				+ 2*cos(pi*cx/((double) (h-1))) - 2; 
        }
    }
	    
	double *f3 = new double[(h-2)*(w-2)];
    double *f3_transp = new double[(h-2)*(w-2)];
    for(int ix = 0 ; ix < (w-2)*(h-2) ;ix++)
    {
		m_transp[ix] = m_transp[ix]/temp[ix];
    }
    idst(m_transp,f3,h-2,w-2);
	transposition(f3,f3_transp,h-2,w-2);
    idst(f3_transp,f3,w-2,h-2);
    transposition(f3,f3_transp,w-2,h-2);

	delete[] m_transp;
	delete[] temp;
	delete[] f3;

	double *destImage = new double[(h)*(w)];
    for(int i = 0 ; i < h;i++)
    {
        for(int j = 0 ; j < w; j++)
        {
            destImage[i*w + j] = (double)((uchar*)(img->imageData + img->widthStep*i))[j];
        }
    }
    for(int i = 1 ; i < h-1;i++)
    {
        for(int j = 1 ; j < w-1; j++)
        {
            destImage[i*w + j] = 0.0;        
        }
    }
    
    for(int i = 1,id1=0 ; i < h-1;i++,id1++)
    {
        for(int j = 1,id2=0 ; j < w-1; j++,id2++)
        {
            destImage[i*w + j] = f3_transp[id1*(w-2) + id2];        
        }
    }
        
	delete[] f3_transp;

    for(int i = 0 ; i < h;i++)
    {
        for(int j = 0 ; j < w; j++)
        {
            if(destImage[i*w + j] < 0.0)
				output.at<uchar>(i,j) = 0;
            else if(destImage[i*w + j] > 255.0)
				output.at<uchar>(i,j) = 255.0;
            else
				output.at<uchar>(i,j) = destImage[i*w + j];        
        }
    }

	delete[] destImage;
};

//---------------------------------
//calculate gradient in x direction
//---------------------------------
void getGradientx(IplImage *img, IplImage *gradx)
{
    int w = img->width;
    int h = img->height;
    int channel = img->nChannels;
    cvZero(gradx);
    for(int i=0;i<h;i++)
	{
        for(int j=0;j<w-1;j++)
		{
            for(int c=0;c<channel;++c)
            {
				((float*)(gradx->imageData + gradx->widthStep*i))[j*channel+c] =
					((uchar*)(img->imageData + img->widthStep*i))[(j+1)*channel+c] -
					((uchar*)(img->imageData + img->widthStep*i))[j*channel+c];
            }
		}
	}
};


//---------------------------------
//calculate gradient in y direction
//---------------------------------
void getGradienty(IplImage *img, IplImage *grady)
{
    int w = img->width;
    int h = img->height;
    int channel = img->nChannels;
    cvZero(grady);
    for(int i=0;i<h-1;i++)
	{
        for(int j=0;j<w;j++)
		{
            for(int c=0;c<channel;++c)
            {
				((float*)(grady->imageData + grady->widthStep*i))[j*channel+c] =
					((uchar*)(img->imageData + img->widthStep*(i+1)))[j*channel+c] -
					((uchar*)(img->imageData + img->widthStep*i))[j*channel+c];                      
            }
		}
	}
};


//--------------------------
//laplacian operator
//--------------------------
void lap(const IplImage *fx, IplImage *gx, const IplImage *fy, IplImage *gy)
{
	
    int w = fx->width;
    int h = fx->height;
    int channel = fx->nChannels;
	cvZero(gx);
    cvZero(gy);
	// y direction
    for(int i=0;i<h;i++)
	{
		for(int j=0;j<w-1;j++)
		{
            for(int c=0;c<channel;++c)
            {
				((float*)(gx->imageData + gx->widthStep*i))[(j+1)*channel+c] =
					((float*)(fx->imageData + fx->widthStep*i))[(j+1)*channel+c] -
					((float*)(fx->imageData + fx->widthStep*i))[j*channel+c];
            }
		}
	}
	w = fy->width;
    h = fy->height;
    channel = fy->nChannels;
	// x direction
    for(int i=0;i<h-1;i++)
	{
        for(int j=0;j<w;j++)
		{
            for(int c=0;c<channel;++c)
            {
				((float*)(gy->imageData + gy->widthStep*(i+1)))[j*channel+c] =
					((float*)(fy->imageData + fy->widthStep*(i+1)))[j*channel+c] -
					((float*)(fy->imageData + fy->widthStep*i))[j*channel+c];
			}              
		}
	}
};

void dst(double *input, double *output,int h,int w)
{
    Mat temp = Mat(2*h+2,1,CV_32F);
    Mat this_result  = Mat(h,1,CV_32F);

    int p=0;
    for(int i=0;i<w;i++)
    {
        temp.at<float>(0,0) = 0.0;
                
        for(int j=0,r=1;j<h;j++,r++)
        {
			temp.at<float>(r,0) = input[j*w+i];
        }

        temp.at<float>(h+1,0)=0.0;

        for(int j=h-1, r=h+2;j>=0;j--,r++)
        {
			temp.at<float>(r,0) = -1*input[j*w+i];
        }
                
        Mat planes[] = {Mat_<float>(temp), Mat::zeros(temp.size(), CV_32F)};

        Mat complex1;
        merge(planes, 2, complex1);

        dft(complex1,complex1,0,0);

        Mat planes1[] = {Mat::zeros(complex1.size(), CV_32F), Mat::zeros(complex1.size(), CV_32F)};
                
        split(complex1, planes1); 

        std::complex<double> two_i = std::sqrt(std::complex<double>(-1));

        double fac = -2*imag(two_i);

        for(int c=1,z=0;c<h+1;c++,z++)
        {
			this_result.at<float>(z,0) = planes1[1].at<float>(c,0)/fac;
        }

        for(int q=0,z=0;q<h;q++,z++)
        {
			output[q*w+p] =  this_result.at<float>(z,0);
        }
        p++;
    }
};


void idst(double *input, double *output,int h,int w)
{
	int nn = h+1;
	unsigned long int idx;
	dst(input,output,h,w);
	for(int  i= 0;i<h;i++)
	{
		for(int j=0;j<w;j++)
		{
			idx = i*w + j;
			output[idx] = (double) (2*output[idx])/nn;
		}
	}
};


void transposition(double *input, double *output,int h,int w)
{
    Mat temp = Mat(h,w,CV_32FC1);
    for(int i = 0 ; i < h;i++)
    {
        for(int j = 0 ; j < w; j++)
        {
            temp.at<float>(i,j) = input[i*w+j];
        }
    }
    Mat transposition = temp.t();
    for(int i = 0;i < transposition.size().height; i++)
	{
        for(int j=0;j<transposition.size().width;j++)
        {
            output[i*transposition.size().width + j] = transposition.at<float>(i,j);
        }
	}
};

};