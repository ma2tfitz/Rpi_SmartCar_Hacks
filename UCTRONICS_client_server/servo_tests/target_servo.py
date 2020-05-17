#!/usr/bin/env python3

# pigpiod must be running on port 8888

import cv2
import numpy as np
import sys
import time
import pigpio

SERVO = 21

MIN_PW = 500
MID_PW = 1500
MAX_PW = 2500

def get_pw_for_tx(tx):
    dx = int((tx - 320)/320.0*1000 + 1500)
    dx = max(MIN_PW, dx)
    dx = min(MAX_PW, dx)
    return 3000 - dx

pi = pigpio.pi('localhost', 8888)
cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()

    blur_img = cv2.blur(img, (13,13))
    hsv_img = cv2.cvtColor(blur_img, cv2.COLOR_BGR2HSV)
    green_low = np.array([30, 100, 20])
    green_high = np.array([45, 255, 255])
    mask_img = cv2.inRange(hsv_img, green_low, green_high)

    im2, contours, hier = cv2.findContours(mask_img, 1, 2)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        r = float(w)/h
        ta = w * h
        if r < 0.8 or r > 1.25 or ta < 500:
            continue
        tx = x + int(w/2)
        ty = y + int(h/2)
        # print(x,y,w,h,w*h,float(w)/h, float(h)/w)
        x1, x2, y1, y2 = x, x+w, y, y+h
        blur_img[y1:y2, x1:x2] = img[y1:y2, x1:x2]
        #blur_img[160:480, 120:360] = img[160:480, 120:360]
        cv2.rectangle(blur_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.circle(blur_img, (tx, ty), 1, (0, 0, 255), 5)
        print(ta, tx, ty)

    cv2.imshow("gray", blur_img)
    pw = get_pw_for_tx(tx)

    pi.set_servo_pulsewidth(SERVO, pw)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
sys.exit(1)
    
