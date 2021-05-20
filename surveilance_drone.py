from djitellopy import tello
import cv2
import numpy as np
import face_recognition as fr
from win32com.client import Dispatch
import keyboard
import time
import sys
import os
from multiprocessing import Process, Pool
import threading

# Connect to Tello
tello = tello.Tello()
tello.connect()
tello.streamon()

# Defining Speak "function"
speak = Dispatch('SAPI.SpVoice').Speak

# Constant Variables
WIDTH = 320
HEIGHT = 240
start_state = True

# Encoding Images
george_image = fr.load_image_file('images/george.jpg')
george_face_encoding = fr.face_encodings(george_image)[0]
voula_image = fr.load_image_file('images/voula.jpg')
voula_face_encoding = fr.face_encodings(voula_image)[0]
dimitri_image = fr.load_image_file('images/dimitri.jpg')
dimitri_face_encoding = fr.face_encodings(dimitri_image)[0]
dylan_image = fr.load_image_file('images/dylan.jpg')
dylan_face_encoding = fr.face_encodings(dylan_image)[0]
kai_image = fr.load_image_file('images/kai.jpg')
kai_face_encoding = fr.face_encodings(kai_image)[0]
salvati_image = fr.load_image_file('images/salvati.jpg')
salvati_face_encoding = fr.face_encodings(kai_image)[0]

known_face_encondings = [george_face_encoding, voula_face_encoding, dimitri_face_encoding, dylan_face_encoding, kai_face_encoding, salvati_face_encoding]
known_face_names = ['George', 'Voula', 'Dimitri', 'Dylan', 'Kai', 'Salvati'] # Enter person name

def cv2_rectangle(frame, left, top, right, bottom, name):
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

def face_recognition():
    while True:
        img = tello.get_frame_read().frame
        img = cv2.resize(img, (360, 240))
        cv2.waitKey(1)

        frame = img

        rgb_frame = frame[:, :, ::-1]

        face_locations = fr.face_locations(rgb_frame)
        face_encodings = fr.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

            matches = fr.compare_faces(known_face_encondings, face_encoding)

            name = 'Unknown'

            face_distances = fr.face_distance(known_face_encondings, face_encoding)

            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                speak(f'Hello {name}')
                # cv2.rectangle(frame=frame, left=left, top=top, right=right, bottom=bottom, name=name)
                # cv2.imwrite(f'people/')

                if name == 'George':
                    # cv2.imwrite(f'people/george/george.jpg', frame)
                    print('Hello George')
                    speak('Would you like to fly the drone?')

                if name == 'Voula':
                    speak('Can you please make the cookie dough?')

                if name == 'Dimitri':
                    speak('Hi dad!')

                if name == 'Dylan':
                    speak("You're a clown")

                if name == 'Kai':
                    speak('You suck at chess')

                if name == 'Salvati':
                    speak('Mid Piece')
        try:
            frame = cv2.resize(frame, (360, 240))
        except:
            pass
        try:
            cv2.putText(frame, f'Hello {name}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        except:
            pass
        cv2.imshow('Which person am I?', frame)

def get_keyboard_input():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 100

    # while True:
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

def video_feed():
    pass
    # while True:
    #     img = tello.get_frame_read().frame
    #     img = cv2.resize(img, (360, 240))
    #     cv2.waitKey(1)

        # frame = img
        #
        # rgb_frame = frame[:, :, ::-1]
        #
        # face_locations = fr.face_locations(rgb_frame)
        # face_encodings = fr.face_encodings(rgb_frame, face_locations)
        #
        # for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        #
        #     matches = fr.compare_faces(known_face_encondings, face_encoding)
        #
        #     name = 'Unknown'
        #
        #     face_distances = fr.face_distance(known_face_encondings, face_encoding)
        #
        #     best_match_index = np.argmin(face_distances)
        #     if matches[best_match_index]:
        #         name = known_face_names[best_match_index]
        #         speak(f'Hello {name}')
        #         cv2_rectangle(frame=frame, left=left, top=top, right=right, bottom=bottom, name=name)
        #     cv2.imshow('Image', frame)


if __name__ == '__main__':
    t1 = threading.Thread(target=face_recognition)
    t2 = threading.Thread(target=video_feed)

# old_stdout = sys.stdout # backup current stdout
# sys.stdout = open(os.devnull, "w")
#
# tello.send_rc_control()
#
# sys.stdout = old_stdout # reset old stdout

t1.start()
t2.start()

while True:
    vals = get_keyboard_input()
    tello.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    time.sleep(0.05)
