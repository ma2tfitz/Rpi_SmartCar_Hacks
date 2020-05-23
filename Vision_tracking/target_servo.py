#!/usr/bin/env python3
import cv2
import numpy as np
import sys
import time
import pigpio

SERVO_X = 4
SERVO_Y = 25


MIN_PW = 600
MID_PW = 1500
MAX_PW = 2000

def get_pw_for_tx(tx):
    dx = 1500 - tx
    dx = max(MIN_PW, dx)
    dx = min(MAX_PW, dx)
    return dx

def get_pw_for_ty(ty):
    dy = tx + 1500
    dy = max(MIN_PW, dy)
    dy = min(MAX_PW, dy)
    return dy

def update_angles(angle_x, angle_y, tx, ty):
    angle_x += -int(tx/8.0) # 8
    angle_y += int(ty/10.0) # 10

    angle_x = max(MIN_PW, angle_x)
    angle_x = min(MAX_PW, angle_x)
    angle_y = max(MIN_PW, angle_y)
    angle_y = min(MAX_PW, angle_y)

    return angle_x, angle_y

pi = pigpio.pi('localhost', 8888)
cap = cv2.VideoCapture(0)


if False:
    # live cam
    green_low = np.array([30, 100, 60])
    green_high = np.array([45, 255, 255])
else:
    # pi cam
    green_low = np.array([35, 100, 80])
    green_high = np.array([75, 255, 255])

tx = 0
ty = 0

angle_x = 1600
angle_y = 1500

pi.set_servo_pulsewidth(SERVO_X, angle_x)
pi.set_servo_pulsewidth(SERVO_Y, angle_y)

while True:
    ret, img = cap.read()

    blur_img = cv2.blur(img, (13,13))
    hsv_img = cv2.cvtColor(blur_img, cv2.COLOR_BGR2HSV)
    mask_img = cv2.inRange(hsv_img, green_low, green_high)

    im2, contours, hier = cv2.findContours(mask_img, 1, 2)

    if  not contours:
        cv2.imshow("gray", blur_img)
        continue

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        r = float(w)/h
        ta = w * h
        if r < 0.8 or r > 1.25 or ta < 500:
            continue
        cx = x + int(w/2)
        cy = y + int(h/2)
        tx = cx - 320
        ty = cy - 240
        # print(x,y,w,h,w*h,float(w)/h, float(h)/w)
        x1, x2, y1, y2 = x, x+w, y, y+h
        blur_img[y1:y2, x1:x2] = img[y1:y2, x1:x2]
        #blur_img[160:480, 120:360] = img[160:480, 120:360]
        cv2.rectangle(blur_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.circle(blur_img, (cx, cy), 1, (0, 0, 255), 5)

    cv2.imshow("gray", blur_img)

    #px = get_pw_for_tx(tx)
    #py = get_pw_for_ty(ty)


    angle_x, angle_y = update_angles(angle_x, angle_y, tx, ty)

    print(ta, tx, ty, angle_x, angle_y)

    pi.set_servo_pulsewidth(SERVO_X, angle_x)
    pi.set_servo_pulsewidth(SERVO_Y, angle_y)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
sys.exit(1)
    
