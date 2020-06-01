#include "InpaintImage.h"
#include "math.h"

using namespace std;

Inpaint::Inpaint(void)
{
	input = NULL;
	mask = NULL;
}

Inpaint::~Inpaint(void)
{
}


//---------------------------------------------------------
// Inpaint image
//---------------------------------------------------------
bool Inpaint::Inpainting(float *srcimg, BYTE *maskimg, int srcwidth, int srcheight, int base_radius)
{

	if(!srcimg || !maskimg || srcwidth <= 0 || srcheight <= 0 )
		return false;

	input = srcimg;
	width  = srcwidth;
	height  = srcheight;
	mask = maskimg;

	float *patchpriority = NULL;
	patchpriority = new float [width*height];

	// set a ROI(patch) to fill
	RECT Roi;
	Roi.left = 0;
	Roi.top = 0;
	Roi.right = width-1;
	Roi.bottom = height-1;

	int fillarea  = base_radius < 4 ? 4 : base_radius;
	int searcharea = fillarea + 15*base_radius;
	float norm = 1.0f/(3*255.0f);

	//calculate the priority for each pixel
	Priority(patchpriority, Roi, fillarea, norm);

	int x, y;
	RECT updatearea;

	while(true) //Loop until entire fill region has been covered
	{
		Roi = FindROIMaxPriority(&x, &y, patchpriority, Roi);
		if(x < 0 || y < 0)
			break;
		if(!FindBestExemplar(&updatearea, x, y, fillarea, searcharea))
			break;

		Priority(patchpriority, updatearea, fillarea, norm);

	}

	delete[] patchpriority;
	return true;
}

//---------------------------------------------------------
// Calculate the piority for each pixel inside the patch
// priority = confidence term * data term
//---------------------------------------------------------
void Inpaint::Priority(float *priority, RECT Roi, int fillarea, float norm)
{
	long startpoint = Roi.top*width + Roi.left;
	float *patchpriority = priority + startpoint;

	BYTE  *maskpx = mask + startpoint;
	BYTE *maskpx_top, *maskpx_botm;

	float *inputpx = input + startpoint*3;
	float *inputpx_top, *inputpx_botm;

	long offset_mask = width - (Roi.right-Roi.left+1);
	long offset_input = offset_mask*3;
	long x0, x1;
	float Ix, Iy, Nx, Ny, temp;

	for(long j = Roi.top; j <= Roi.bottom; j++, patchpriority += offset_mask, maskpx += offset_mask, inputpx += offset_input)
	{
		// top and bottom boundary cases
		if(j > 0)
		{
			maskpx_top = maskpx - width;
			inputpx_top = inputpx - width*3;
		}
		else
		{
			maskpx_top = maskpx;
			inputpx_top = inputpx;
		}

		if(j < height-1)
		{
			maskpx_botm = maskpx + width;
			inputpx_botm = inputpx + width*3;
		}
		else
		{
			maskpx_botm = maskpx;
			inputpx_botm = inputpx;
		}


		for(long i = Roi.left; i <= Roi.right; i++, patchpriority++, maskpx++, maskpx_top++, maskpx_botm++)
		{
			//pixels inside the mask area (white area) bring down the piority of the ROI(patch)
			if(*maskpx == COLOR_MASK)
			{
				inputpx += 3; inputpx_top += 3; inputpx_botm += 3;
				*patchpriority = -1;
				continue;
			}

			// left and right boundary cases
			if(i > 0)
				x0 = -1;
			else
				x0 = 0;
			if(i < width-1)
				x1 = 1;
			else
				x1 = 0;

			//if a pixel and its 8 neighbors are outside of the mask area (white area), bring down the piority
			if(maskpx_top[x0] == (*maskpx) && (*maskpx_top) == (*maskpx) && maskpx_top[x1] == (*maskpx)
				&& maskpx[x0]  == (*maskpx) && maskpx[x1] == (*maskpx)
				&& maskpx_botm[x0] == (*maskpx) && (*maskpx_botm) == (*maskpx) && maskpx_botm[x1] == (*maskpx))
			{
				inputpx += 3; inputpx_top += 3; inputpx_botm += 3;
				*patchpriority = -1;
				continue;
			}


			//calculate confidence
			*patchpriority = Confidence(i, j, fillarea);

		   //norm at this pixel
		   Nx = 0.5 * (maskpx[x0] - maskpx[x1]);
		   Ny = 0.5 * ((*maskpx_top) - (*maskpx_botm));
		   if(Nx == 0.0f && Ny == 0.0f)
		   {
			   inputpx += 3; inputpx_top += 3; inputpx_botm += 3;
			   (*patchpriority) *= 0.001;
			   continue;
		   }
		   if(Nx == 0.0f)
			   Ny = Ny < 0.0f ? -1.0f : 1.0f;
		   else if(Ny == 0.0f)
			   Nx = Nx < 0.0f ? -1.0f : 1.0f;
		   else
		   {
			   Nx  = Nx < 0.0f ? -0.70710678f : 0.70710678f;
			   Ny  = Ny < 0.0f ? -0.70710678f : 0.70710678f;
		   }

		   //Initialize isophote value at this pixel
		   Ix = Iy = 0.0f;
		   for(long k = 0; k < 3; k++, inputpx++, inputpx_top++, inputpx_botm++)
		   {
			   Ix += 0.5 * ((i < width-1 ? inputpx[3] : inputpx[0]) - (i > 0 ? inputpx[-3] : inputpx[0]));
			   Iy += 0.5 * ((*inputpx_botm) - (*inputpx_top));
		   }
		   Ix *= norm;
		   Iy *= norm;

		   //rotate gradient 90 degrees
		   temp = Ix;
		   Ix = -Iy;
		   Iy = temp;

		   //multiply the data term
		   (*patchpriority) *= (fabs(Ix*Nx + Iy*Ny) + 0.001);
		}
	}
}

//---------------------------------------------------------
// Calculate the confidence term
//---------------------------------------------------------
float Inpaint::Confidence(int x, int y, int fillarea)
{
	RECT roi;
	roi.left  = max(0, x - fillarea);
	roi.top  = max(0, y - fillarea);
	roi.right = min(width-1, x + fillarea);
	roi.bottom = min(height-1, y + fillarea);

	int conf = 0, size = 0;
	long offset = width - (roi.right - roi.left+1);
	BYTE *maskpx = mask + roi.top * width + roi.left;

	for(long j = roi.top; j <= roi.bottom; j++, maskpx += offset)
	{
		for(long i = roi.left; i <= roi.right; i++, maskpx++)
		{
			size++;
			if(*maskpx == COLOR_MASK)
				continue;
			conf++;
		}
	}

	if(size == 0)
		return 0;
	else
		return (float)conf/size;
}


//---------------------------------------------------------
// Find patch with maximum priority
//---------------------------------------------------------
RECT Inpaint::FindROIMaxPriority(int *x, int *y, float *priority, RECT Roi)
{
	RECT newRoi;
	newRoi.left   = Roi.right;
	newRoi.top   = Roi.bottom;
	newRoi.right  = Roi.left;
	newRoi.bottom = Roi.top;

	long offset = width - (Roi.right-Roi.left+1);
	float *p = priority + Roi.top*width + Roi.left;
	float Max = 0;
	*x = *y = -1;
	for(long j = Roi.top; j <= Roi.bottom; j++, p+=offset)
	{
		for(long i = Roi.left; i <= Roi.right; i++, p++)
		{
			if(*p < 0.0f)
			continue;

			if(j < newRoi.top)
				newRoi.top  = j;
			if(j > newRoi.bottom)
				newRoi.bottom = j;
			if(i < newRoi.left)
				newRoi.left  = i;
			if(i > newRoi.right)
				newRoi.right = i;

			if(Max < (*p))
			{
				Max = *p;
				*x  = i;
				*y  = j;
			}
		}
	}
	return newRoi;
}

//---------------------------------------------------------
// Find exemplar that minimizes error and update image data
//---------------------------------------------------------
bool Inpaint::FindBestExemplar(RECT *updateRc, long x, long y, long matchRadius, long searchRadius)
{
	RECT matchRegion, bestexemplar;
	matchRegion.left  = max<long>(0, x - matchRadius);
	matchRegion.right  = min<long>(width-1, x + matchRadius);
	matchRegion.top  = max<long>(0, y - matchRadius);
	matchRegion.bottom = min<long>(height-1, y + matchRadius);
	long matchX  = matchRegion.right - matchRegion.left;
	long matchY  = matchRegion.bottom - matchRegion.top;

	long offset_mask = width - (matchX+1);
	long offset_input = 3*offset_mask;
	long startpixel  = matchRegion.top * width + matchRegion.left;
	float *inputpx = input + startpixel*3;
	BYTE *maskpx = mask + startpixel;

	//Search inside the radius area
	long startx = max(matchRadius, matchRegion.left - searchRadius);
	long endx = min(width-matchRadius, matchRegion.right + searchRadius);
	long starty = max(matchRadius, matchRegion.top - searchRadius);
	long endy = min(height-matchRadius, matchRegion.bottom + searchRadius);

	////search the whole image
	//long startx = matchRadius;
	//long endx = width-matchRadius;
	//long starty = matchRadius;
	//long endy = height-matchRadius;

	float bestErr = 255e10f, patchErr;
	RECT exemplar;
	for(; starty < endy; starty++)
	{
		exemplar.top  = starty - matchRadius;
		exemplar.bottom = exemplar.top + matchY;
		for(long i = startx; i < endx; i++)
		{
			exemplar.left  = i - matchRadius;
			exemplar.right = exemplar.left + matchX;
			if(!IsValid(exemplar))	// do not use as reference if the exemplar contains mask pixels
				continue;

			//Calculate patch error
			patchErr = Difference(exemplar, inputpx, offset_input, maskpx, offset_mask, bestErr);
			if(patchErr < bestErr)
			{
				bestErr = patchErr;
				bestexemplar  = exemplar;
			}
			if(bestErr == 0.0f)
				break;
		}
	}

	//Update image data
	if(bestErr != 255e10f)
	{
		long fillRadius = matchRadius;
		RECT tofill;
		tofill.left  = max<long>(0, x - fillRadius);
		tofill.right = min<long>(width-1, x + fillRadius);
		tofill.top  = max<long>(0, y - fillRadius);
		tofill.bottom = min<long>(height-1, y + fillRadius);

		*updateRc = tofill;
		Update(bestexemplar, tofill);
		return true;
	}

	return false;
}

//---------------------------------------------------------
// Update image data
//---------------------------------------------------------
void Inpaint::Update(RECT bestexemplar, RECT tofill)
{
	long offset_mask = width - (tofill.right - tofill.left + 1);
	long offset_input = offset_mask*3;
	long startpoint = tofill.top*width + tofill.left;
	float *bestpx = input + (bestexemplar.top*width + bestexemplar.left)*3;
	float *inputpx = input + startpoint*3;
	BYTE  *maskpx = mask + startpoint;
	for(long j = bestexemplar.top; j <= bestexemplar.bottom; j++, inputpx += offset_input, bestpx += offset_input, maskpx += offset_mask)
	{
		for(long i = bestexemplar.left; i <= bestexemplar.right; i++, maskpx++)
		{
			if(*maskpx != COLOR_MASK)
			{
				bestpx += 3;
				inputpx += 3;
				continue;
			}

			for(long k = 0; k < 3; k++, bestpx++, inputpx++)
			{
				*maskpx = COLOR_FILL; //fill mask with black
				*inputpx = *bestpx;	//fill image with bestexemplar
			}
		}
	}
}

//------------------------------------------------------------------------------
// Calculate the differences between the exemplar and the patch to be filled
//------------------------------------------------------------------------------
float Inpaint::Difference(RECT exemplar, float *inputpx, long offset_input, BYTE *maskpx, long offset_mask, float bestErr)
{
	float diff = 0.0f;
	float *px_input = inputpx;
	float *px_exemplar = input + (exemplar.top*width + exemplar.left)*3;
	BYTE  *thismaskpx  = maskpx;
	for(long j = exemplar.top; j <= exemplar.bottom; j++, px_input += offset_input, px_exemplar += offset_input, thismaskpx += offset_mask)
	{
		for(long i = exemplar.left; i <= exemplar.right; i++, thismaskpx++)
		{
			if(*thismaskpx == COLOR_MASK)
			{
				px_input += 3;
				px_exemplar += 3;
				continue;
			}

			for(long k = 0; k < 3; k++, px_input++, px_exemplar++)
				diff += fabs((*px_input) - (*px_exemplar));

			if(diff > bestErr)
				break;
		}
	}
	return diff;
}

//------------------------------------------------------------------
// Decide if the exemplar is valid (contains any white mask pixels)
//------------------------------------------------------------------
bool Inpaint::IsValid(RECT exemplar)
{
	long offset = width - (exemplar.right-exemplar.left+1);
	BYTE *maskpx = mask + exemplar.top*width + exemplar.left;
	bool is_valid = (*maskpx) != COLOR_MASK;
	for(long j = exemplar.top; is_valid && j <= exemplar.bottom; j++, maskpx += offset)
	{
		for(long i = exemplar.left; is_valid && i <= exemplar.right; i++, maskpx++)
			is_valid = (*maskpx) != COLOR_MASK;
	}
	return is_valid;
}
