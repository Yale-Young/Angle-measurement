import cv2 as cv
import numpy as np
import math

def angle(v1, v2):
  dx1 = v1[2] - v1[0]
  dy1 = v1[3] - v1[1]
  dx2 = v2[2] - v2[0]
  dy2 = v2[3] - v2[1]
  angle1 = math.atan2(dy1, dx1)
  angle1 = int(angle1 * 180/math.pi)
  angle2 = math.atan2(dy2, dx2)
  angle2 = int(angle2 * 180/math.pi)
  if angle1*angle2 >= 0:
    included_angle = abs(angle1-angle2)
  else:
    included_angle = abs(angle1) + abs(angle2)
    if included_angle > 180:
      included_angle = 360 - included_angle
  return included_angle



cap = cv.VideoCapture("test.mp4")
f = 0
while (cap.isOpened()):
    f+=1
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
    ret1, thresh1 = cv.threshold(gray, 180, 255, cv.THRESH_BINARY)
    thresh1 = cv.medianBlur(thresh1, 5)
    blur = cv.blur(thresh1, (25, 25))
    kernel = np.ones((20, 20), np.uint8)
    blur = cv.dilate(blur, kernel)
    image, contours, hierarchy = cv.findContours(blur, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    nums = len(contours)
    hull = cv.convexHull(contours[nums-1])
    nn = len(hull)
    si =0
    list = np.array([[[0,0]],[[0,0]],[[0,0]],[[0,0]],[[0,0]],[[0,0]]])
    s=0
    for i in range(0,nn):
        flag =0
        for j in range(0,len(list)):
            if abs(list[j][0][0]-hull[i][0][0])+abs(list[j][0][1]-hull[i][0][1])<180:
                list[j][0][0] = (list[j][0][0]+hull[i][0][0])/2
                list[j][0][1]=(list[j][0][1]+hull[i][0][1])/2
                flag =1
                break
        if flag == 0 :
            list[s][0]=hull[i][0]
            s = s + 1
    if s!= 6:
        for l in range(s,6):
            list=np.delete(list,s,0)
    xs = 0
    ys = 0
    le=len(list)
    for k in range(0,le):
        xs += list[k][0][0]
        ys += list[k][0][1]
    x = int(xs/le)
    y = int(ys/le)
    print(f,end="\t")
    for k in range(0, le):
        cv.line(thresh1, (x, y), (list[k][0][0],list[k][0][1]), (255), 5)
        if k!=le-1 :
            a = angle((x, y,list[k][0][0],list[k][0][1]),(x, y,list[k+1][0][0],list[k+1][0][1]))
        else: a = angle((x, y,list[k][0][0],list[k][0][1]),(x, y,list[0][0][0],list[0][0][1]))
        a1 =list[k][0][0]-5
        a2= list[k][0][1]-5
        cv.putText(thresh1,str(k),(a1,a2), cv.FONT_HERSHEY_SIMPLEX, 2, (255), 3)
        print(a,end='\t')
    cv.polylines(thresh1, [list], True, 255, 2)
    print('')
    cv.imshow("img", thresh1)
    c = cv.waitKey(1)
    if c == 27:
        break
cap.release()
