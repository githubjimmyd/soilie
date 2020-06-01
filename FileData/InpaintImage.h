#pragma once
#define COLOR_MASK 255
#define COLOR_FILL 0

#include <iostream>
#include <stdlib.h>
#include <windows.h>
#include "math.h"


class Inpaint
{
public:
	Inpaint(void);
	~Inpaint(void);

	bool Inpainting(float *srcimg, BYTE *maskimg, int srcwidth, int srcheight, int base_radius);
	void Priority(float *priority, RECT Roi, int fillarea, float norm);
	float Confidence(int x, int y, int fillarea);
	RECT FindROIMaxPriority(int *x, int *y, float *priority, RECT Roi);
	bool FindBestExemplar(RECT *updateRc, long x, long y, long matchRadius, long searchRadius);
	void Update(RECT bestexemplar, RECT tofill);
	float Difference(RECT exemplar, float *inputpx, long offset_input, BYTE *maskpx, long offset_mask, float bestErr);
	bool IsValid(RECT exemplar);

private:
	float *input;
	int width, height;
	BYTE *mask;
};