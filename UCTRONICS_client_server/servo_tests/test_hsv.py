#!/usr/bin/env python3
import cv2
import numpy as np
import sys
import time

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    #gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur_img = cv2.blur(img, (3,3))
    hsv_img = cv2.cvtColor(blur_img, cv2.COLOR_BGR2HSV)
    green_low = np.array([30, 100, 20])
    green_high = np.array([45, 255, 255])
    mask_img = cv2.inRange(hsv_img, green_low, green_high)
    #gray[mask_img > 0] = (75,255,200)

    im2, contours, hier = cv2.findContours(mask_img, 1, 2)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        r = float(w)/h
        if r < 0.8 or r > 1.25 or w*h < 500:
            continue
        # print(x,y,w,h,w*h,float(w)/h, float(h)/w)
        cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 2)
        tx = x + int(w/2)
        ty = y + int(h/2)
        cv2.circle(img, (tx, ty), 1, (0, 0, 255), 5)
    cv2.imshow("gray", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
sys.exit(1)
    

img = cv2.imread('test.jpg', cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_blurred = cv2.blur(gray, (3,3))
gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
green_low = np.array([30, 180, 60])
green_high = np.array([45, 255, 255])
mask_img = cv2.inRange(hsv_img, green_low, green_high)
gray[mask_img > 0] = (75,255,200)

im2, contours, hier = cv2.findContours(mask_img, 1, 2)

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    r = float(w)/h
    if r < 0.8 or r > 1.25 or w*h < 500:
        continue
    print(x,y,w,h,w*h,float(w)/h, float(h)/w)
    cv2.rectangle(gray, (x,y), (x+w, y+h), (0, 0, 255), 2)
    cv2.imshow("gray", gray)
    cv2.waitKey(1000)
    
res = cv2.bitwise_and(img, img, mask=mask_img)

cv2.imshow("mask", mask_img)
cv2.waitKey(2000)
cv2.imshow("img", img)
cv2.waitKey(2000)
cv2.imshow("HSV", hsv_img)
cv2.waitKey(2000)

gray_blurred = cv2.blur(gray, (3,3))

detected_circles = cv2.HoughCircles(gray_blurred,
                                    cv2.HOUGH_GRADIENT, 1, 20,
                                    param1=50, param2=30,
                                    minRadius=1, maxRadius=40)

if detected_circles is not None:
    detected_circles = np.uint16(np.around(detected_circles))
    cv2.imshow("Detected Circles", img)
    cv2.waitKey(2000)
    for pt in detected_circles[0,:]:
        a, b, r = pt[0], pt[1], pt[2]
        if a == 158:
            continue
        print(a, b, r)
        cv2.circle(img, (a, b), r, (0, 255, 0), 2)
        cv2.circle(img, (a, b), 1, (255, 0, 0), 3)
        cv2.imshow("Detected Circles", img)
        cv2.waitKey(1000)
    cv2.waitKey(2000)

