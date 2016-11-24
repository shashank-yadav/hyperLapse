from fMatch import *

w = 25
g = 25
v = 16
batchSize = 200
lamdaS = 10
lamdaA = 10

inputFile = 'videoplayback.mp4'
# inputFile = 'roadedge0.mp4'
# inputFile = 'run.mp4'
outptFile = 'Hyperlapse' + inputFile.split('.')[0] + '.avi'
# cap = cv2.VideoCapture("test.mp4")
cap = cv2.VideoCapture(inputFile)
ret, frame = cap.read()
temporalNeighbors = np.zeros([batchSize,frame.shape[0],frame.shape[1]],dtype = np.uint8)
fCount = 0
it = 0
MCList = []

while ret:
	
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	if it == batchSize:
		motionCostArr = np.zeros(w)
		for i in xrange(0,batchSize-w):
			fi = temporalNeighbors[i,:,:]
			fjList = temporalNeighbors[range(i+1,i+w+1),:,:]
			MCList.append(CmList(fi,fjList))

		temporalNeighbors[range(0,w),:,:] = temporalNeighbors[range(batchSize-w,batchSize),:,:]
		it = w 		

	temporalNeighbors[it,:,:] = frame
	it += 1
	ret, frame = cap.read()
	print fCount
	fCount += 1

motionCostArr = np.zeros(w)
print len(MCList)
for i in xrange(0,it-w):
	fi = temporalNeighbors[i,:,:]
	fjList = temporalNeighbors[range( i+1 , i+w+1),:,:]
	toAppend = CmList(fi,fjList)
	# if len(toAppend) > 0:
	MCList.append(toAppend)



# Initialization
D = np.zeros([len(MCList),w])
T = np.zeros([len(MCList),w])

for i in xrange(0,g):
	for j in xrange(0,w):
		D[i,j] = MCList[i][j]+ lamdaS*Cs(i,j+i+1,v)


# First pass: populate Dv
for i in xrange(g,len(MCList)):
	for j in xrange(0,w):
		c = MCList[i][j] + lamdaS*Cs(i,j+i+1,v)
		minVal , argmin = getMin( D, i , j+i+1 ,lamdaA )
		D[i,j] = c + minVal
		T[i,j] = argmin


# Second pass: trace back min cost path
t = len(MCList)

s = -1
d = -1
minVal = float("inf")

for i in xrange(t-g,t):
	for j in xrange(0,w):
		print i,j,D[i,j]
		if D[i,j] < minVal:
			minVal = D[i,j] 
			s,d = i,j

p = [s+d+1]
while s > g:
	p.append(s)
	b = T[s,d]
	d = s - (b+1)
	s = b

p.reverse()

cap = cv2.VideoCapture(inputFile)
ret, frame = cap.read()
fCount = 0
it = 0
fourcc = cv2.cv.CV_FOURCC(*'XVID')
size = (frame.shape[1], frame.shape[0])
vid = cv2.VideoWriter(outptFile, fourcc, 10 , size, True)


while ret and it < len(p): 
	if fCount == p[it]:
		vid.write(frame)
		it += 1
	ret,frame = cap.read()
	print fCount
	fCount += 1


vid.release()
