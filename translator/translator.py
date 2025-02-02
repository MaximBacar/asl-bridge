'''
Generate a sequence

- the user starts and is prompted to make the first word of its sentence
- the user has 30 frames to produce one word
- the user presses space, to get to the next word of his sentence
- the user presses backspace to restart

- in all cases a 5 seconds countdown is shown before starting the lecture

- once the user is done with his sentence, he presses enter

- the phrase is converted to spoken english

'''


import cv2 as cv
import numpy as np

import body_tracking
import time

from    tensorflow.keras.models import load_model

from conversation_utils import Conversation

CAPTURE_TIMER       = 5
FRAME_PER_SEQUENCE  = 30
WORDS_PATH          = "translator/words.txt"


def load_words():
    with open(WORDS_PATH, "r") as file:
        words = file.readlines()

    words = [word.strip() for word in words]
    return words

sentence        = []
camera          = cv.VideoCapture(0)
model           = load_model('model-training/new3.keras')
words           = load_words()

status          = 0
timer_start     = -1
capture_count   = 0
sequence        = []
word            = ""
draw_squeleton  = False

conversation             = Conversation()


def asl_to_written( asl : str ) -> str:
    # ChatGPT api, ask to translate the ASL sentence to words
    # return sentence
    return ""

def read_text( text : str ) -> str:
    # Elevenlabs API
    pass

# 0 : idle, 1 : countdown, 2: recording

with body_tracking.mp_h.Holistic(min_detection_confidence=0.5,  min_tracking_confidence=0.5) as holistic:
    while camera.isOpened():

        _, frame = camera.read()
        image, results  = body_tracking.mediapipe_detection( frame, holistic )

        # IDLE
        if status == 0:
            cv.putText(image, "PRESS SPACE TO START", (750,500), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv.LINE_AA)

        # Countdown
        if status == 1:
            elapsed_time = time.perf_counter() - timer_start

            countdown = int(CAPTURE_TIMER - elapsed_time)
            cv.putText(image, f"{countdown}", (750,500), cv.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 2, cv.LINE_AA)

            if elapsed_time > CAPTURE_TIMER:
                status = 2

        # Recording
        if status == 2:

            data            = body_tracking.transform_data( results )

            sequence.append(data)

            capture_count += 1

            if capture_count > FRAME_PER_SEQUENCE:
                result = model.predict(np.expand_dims(sequence, axis=0))[0]
                print(result)
                word = words[np.argmax(result)]
                status = 3
        
        if status == 3:
            cv.putText(image, f"{word}", (750,500), cv.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 2, cv.LINE_AA)
            cv.putText(image, f"PRESS SPACE TO RECORD NEXT WORD", (750,550), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv.LINE_AA)
            cv.putText(image, f"PRESS ENTER TO STOP", (750,600), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv.LINE_AA)
            cv.putText(image, f"PRESS BACKSPACE TO RESTART", (750,650), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv.LINE_AA)
        # Press space
        
        key = cv.waitKey(10) & 0xFF
        if key == 32:
            if status == 0:
                status = 1
                timer_start = time.perf_counter()

            if status == 3:
                sentence.append(word)
                sequence.clear()
                word = ""
                capture_count = 0
                timer_start = time.perf_counter()

                # back to countdown
                status = 1

        # Backspace
        if key == ord('r'):
            if status == 3:
                sequence.clear()
                word = ""
                capture_count = 0
                timer_start = time.perf_counter()

                # back to countdown
                status = 1

        # show/hide mask
        if key == ord('q'):
            draw_squeleton = not draw_squeleton

        # Press enter
        if key == 13:
            sentence.append(word)
            sentence_str = " ".join(sentence)
            text = conversation.asl_to_text(sentence_str)
            conversation.text_to_audio(text)
            status = 0 
            word = ''
            capture_count = 0
            sentence.clear()

        if draw_squeleton:
            body_tracking.draw_skeleton(image, results)
        
        cv.imshow('ASL-Bridge', image)

camera.release()
cv.destroyAllWindows()