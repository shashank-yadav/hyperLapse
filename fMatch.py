import cv2
import math
import numpy as np

def CmList(fi,fjList):

	# fi = cv2.cvtColor(fi, cv2.COLOR_BGR2GRAY)
	# fj = cv2.cvtColor(fj, cv2.COLOR_BGR2GRAY)

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

	motionCostArr = np.zeros(fjList.size)
	it = 0

	for fj in fjList:

		# calculate optical flow and
		# Try to find homography
		try:
			p1, st, err = cv2.calcOpticalFlowPyrLK(fi, fj, p0, None, **lk_params)
			good_new = p1[st==1]
			good_old = p0[st==1]
			# print good_old
			if len(good_old) > 10:
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
					pt1[0,0] /= pt1[2,0]
					pt1[1,0] /= pt1[2,0]
					pt1[2,0] = 1


					pt2[0,0] = good_new[x,0]
					pt2[1,0] = good_new[x,1]
					pt2[2,0] = 1

					Cm += np.linalg.norm(pt2-pt1)

				Cm /= good_old.shape[0]
				
				pt1[0,0] = fi.shape[1]/2
				pt1[1,0] = fi.shape[0]/2
				pt1[2,0] = 1
				
				pt2 = np.mat(h)*pt1
				pt2[0,0] /= pt2[2,0]
				pt2[1,0] /= pt2[2,0]
				pt2[2,0] = 1
				
				C0 = np.linalg.norm(pt2-pt1)
				
				# print Cm , C0 , tc , gamma

				if Cm < tc:
					motionCostArr[it] = C0
				else:
					motionCostArr[it] = gamma
			else:
				motionCostArr[it] = gamma	

			it += 1

		#Exception if homography not found
		except Exception, e:
			motionCostArr[it] = gamma
			it += 1


	# print motionCostArr[0]

	return motionCostArr



def Cs(i,j,v):
	ts = 200
	return min(math.fabs((j-i) - v ),ts)



def Ca(h,i,j):
	ta = 200
	return min(math.fabs((j-i) - (i-h) ),ta)


def getMin(D,i,j,lamdaA):
	argmin = 0
	minVal = float("inf")
	l = []
	for k in xrange( 1 , D.shape[1]+1):
		val = D[i-k,k-1] + lamdaA*Ca(i-k,i,j)
		l.append(val)
		if val < minVal:
			minVal = val
			argmin = i-k
	# print l

	return (minVal,argmin) 