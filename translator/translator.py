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


FRAME_PER_SEQUENCE = 30

sentence = []


def record_word() -> str:
    for _ in range(FRAME_PER_SEQUENCE):

        # take pic
        # extract data
        # make prediction

        # return word

        pass


def asl_to_written( asl : str ) -> str:
    # ChatGPT api, ask to translate the ASL sentence to words
    # return sentence
    pass

def read_text( text : str ) -> str:
    # Elevenlabs API
    pass
while(True):
    pass
    # press space to take a pic

    # count down on screen

    # call record_word()

    # return prediction

    # backspace to restart

    # space to go to next pic
    # -> Add word to sentence array
    # -> loops
    
    # enter to stop
    # -> Add word to sentence array
    # -> Exit loop
    # -> call asl_to_written()
    # -> call read_text()

    

    