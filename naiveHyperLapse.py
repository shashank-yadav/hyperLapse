from fMatch import *
import sys

w = 25
g = 25
v = int(sys.argv[2])#16
batchSize = 200
lamdaS = 10
lamdaA = 10

inputFile = str(sys.argv[1])
# inputFile = 'roadedge0.mp4'
# inputFile = 'run.mp4'
outptFile = 'naiveHyperLapse' + inputFile.split('.')[0] + '_' + str(v) + '.avi'

cap = cv2.VideoCapture(inputFile)
ret, frame = cap.read()
fCount = 0
fourcc = cv2.cv.CV_FOURCC(*'XVID')
# fourcc = cv2.videowriter_fourcc(*'XVID')
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
size = (frame.shape[1], frame.shape[0])
vid = cv2.VideoWriter(outptFile, fourcc, 30 , size, True)


while ret: 
	if fCount%v == 0:
		vid.write(frame)
	temp = 0
	ret,frame = cap.read()
	while temp < 5 and ret == False:
		ret,frame = cap.read()
		print temp
		temp += 1
	print fCount , temp , ret
	fCount += 1

print "Done"
cap.release()
vid.release()
