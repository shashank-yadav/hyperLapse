import cv2
import math
import numpy as np

def Cm(fi,fj):

	d = np.sqrt( fi.shape[0]*fi.shape[0] + fi.shape[1]*fi.shape[1] )
	tc = 0.1*d
	gamma = 0.5*d


	# params for ShiTomasi corner detection
	feature_params = dict( maxCorners = 100,
	                        qualityLevel = 0.3,
	                        minDistance = 7,
	                        blockSize = 7 )
	 
	# Parameters for lucas kanade optical flow
	lk_params = dict( winSize  = (15,15),
	                   maxLevel = 2,
	                   criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

	p0 = cv2.goodFeaturesToTrack(fi, mask = None, **feature_params)

	# calculate optical flow
	p1, st, err = cv2.calcOpticalFlowPyrLK(fi, fj, p0, None, **lk_params)
	good_new = p1[st==1]
	good_old = p0[st==1]

	h, status = cv2.findHomography(good_old, good_new)
	
	Cm = 0.0

	pt1 = np.ones([3,1])
	pt2 = np.ones([3,1])
	pt1 = np.asmatrix(pt1)
	pt2 = np.asmatrix(pt2)
	
	for x in xrange(0,good_old.shape[0]):
		pt1[0,0] = good_old[x,0]
		pt1[1,0] = good_old[x,1]
		pt1[2,0] = 1

		pt1 = np.mat(h)*pt1

		pt2[0,0] = good_new[x,0]
		pt2[1,0] = good_new[x,1]
		pt2[2,0] = 1

		Cm += np.linalg.norm(pt2-pt1)

	Cm /= good_old.shape[0]
	
	pt1[0,0] = good_old.shape[0]/2
	pt1[1,0] = good_old.shape[1]/2
	pt1[2,0] = 1
	
	pt2 = np.mat(h)*pt1

	C0 = np.linalg.norm(pt2-pt1)
	
	# print Cm , C0 , tc , gamma

	if Cm < tc:
		return C0
	else:
		return gamma


def Cs(i,j,v):
	ts = 200
	return min(math.fabs((j-i) - v ),ts)



def Ca(h,i,j):
	ta = 200
	return min(math.fabs((j-i) - (i-h) ),ts)
