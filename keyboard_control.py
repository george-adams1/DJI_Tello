from djitellopy import tello
import keyboard
import time
import cv2

# Connect to Tello
tello = tello.Tello()
tello.connect()
print(tello.get_battery())

global airborne
airborne = False

def get_keyboard_input():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 100

    # Left - Right
    if keyboard.is_pressed('a'):
        lr = -speed
    elif keyboard.is_pressed('d'):
        lr = speed

    # Front - Back
    if keyboard.is_pressed('s'):
        fb = -speed
    elif keyboard.is_pressed('w'):
        fb = speed

    # Up - Down
    if keyboard.is_pressed('down'):
        ud = -speed
    elif keyboard.is_pressed('up'):
        ud = speed

    # Turn Clockwise - Counterclockwise
    if keyboard.is_pressed('left'):
        yv = -speed
    elif keyboard.is_pressed('right'):
        yv = speed

    # Landing
    if keyboard.is_pressed('l'):
        tello.land()

    # Takeoff
    if keyboard.is_pressed('q'):
        tello.takeoff()

    # Flip Forward
    if keyboard.is_pressed('f'):
        tello.flip_forward()

    return [lr, fb, ud, yv]

tello.streamoff()
tello.streamon()

while True:
    vals = get_keyboard_input()
    tello.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    time.sleep(0.05)
    img = tello.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow('Image', img)
    cv2.waitKey(1)
