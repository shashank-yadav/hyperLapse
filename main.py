from fMatch import * 

f1 = cv2.imread('road1.png')
f1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)

f2 = cv2.imread('road2.png')
f2 = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)

print Cm(f1,f2)