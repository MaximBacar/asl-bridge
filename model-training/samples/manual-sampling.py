import os
import time
import cv2 as cv
import numpy as np
import  mediapipe   as mp
from    matplotlib  import  pyplot  as plt


collection_location = "/Volumes/SSD"


collection_folder   = os.path.join( collection_location, "collection" )
wordlist_file       = os.path.join(collection_folder, "wordlist.txt")



SAMPLE_TIME_SECONDS = 2
SAMPLE_FRAMES       = 30

camera = cv.VideoCapture(0)


mp_h = mp.solutions.holistic
mp_d = mp.solutions.drawing_utils


def mediapipe_detection( image, model ):
    '''Detect hands and head position
    '''
    image = cv.cvtColor( image, cv.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv.cvtColor( image, cv.COLOR_RGB2BGR)
    return image, results


def draw_skeleton( image, results ):
    '''Draw the detected limbs on screen
    '''
    #mp_d.draw_landmarks( image, results.face_landmarks,         mp_h.FACEMESH_CONTOURS)
    mp_d.draw_landmarks( image, results.left_hand_landmarks,    mp_h.HAND_CONNECTIONS)
    mp_d.draw_landmarks( image, results.right_hand_landmarks,   mp_h.HAND_CONNECTIONS)
    mp_d.draw_landmarks( image, results.pose_landmarks,         mp_h.POSE_CONNECTIONS)


def transform_data( results ):
    '''Error handle the data
    '''
    if results.pose_landmarks:
        pose = np.array([[result.x, result.y, result.z] for result in results.pose_landmarks.landmark]).flatten()
    else:
        pose = np.zeros(99)

    if results.left_hand_landmarks:
        left_h = np.array([[result.x, result.y, result.z] for result in results.left_hand_landmarks.landmark]).flatten() 
    else:
        left_h = np.zeros(63)

    if results.right_hand_landmarks:
        right_h = np.array([[result.x, result.y, result.z] for result in results.right_hand_landmarks.landmark]).flatten()
    else:
        right_h = np.zeros(63)
    
    if results.face_landmarks:
        head = np.array([[result.x, result.y, result.z] for result in results.face_landmarks.landmark]).flatten()
    else:
        head = np.zeros(1404)

    # dont use head
    return np.concatenate([pose, left_h, right_h])


def create_collection_folder():
    if os.path.exists(collection_folder) and os.path.isdir(collection_folder):
        print('Folder already exists')
    else:
        os.mkdir(collection_folder)
        with open(wordlist_file, "w") as file:
            file.write('')


def start_collection( word ):
    dirs = [d for d in os.listdir(collection_folder) if os.path.isdir(os.path.join(collection_folder, d))]

    dir_name = 0

    if dirs:
        max_folder = max(list(map(int, dirs)))
        dir_name = int(max_folder) + 1

    os.mkdir(os.path.join(collection_folder, str(dir_name)))

    with open(wordlist_file, 'a') as file:
        file.write(f"{word}, {dir_name}\n")

    sample_size = 60

    with mp_h.Holistic(min_detection_confidence=0.7,  min_tracking_confidence=0.7) as holistic:
        for sample in range(sample_size):
            good = False
            
            while not good:
                print( "================================================")
                print( f"CURRENT SAMPLE : {sample} PRESS 'S' TO START COLLECTION" )
                print( "================================================")
                i = ''
                while(i != 's'):
                    i = input()

                print()
                print("Collecting ...")
                print()

                for frame in range( SAMPLE_FRAMES ):
                        
                    frame_path = os.path.join(collection_folder, str(dir_name), f"{dir_name}_{sample}_{frame}")
                        # take picture
                    _, frame = camera.read()
                    image, results = mediapipe_detection( frame, holistic )
                    draw_skeleton( image, results )
                    data = transform_data( results )

                    np.save(frame_path, data)
                    #print(data)
                    cv.imshow("ASL", image)

                    if cv.waitKey(10) & 0xFF == ord('q'):
                        break
                        

                    #time.sleep(SAMPLE_TIME_SECONDS / SAMPLE_FRAMES)
                print(f"COMPLETE [{sample}]")

                restart = ''
                while(restart != 'y' and restart != 'n'):
                    restart = input("Restart sample (y/n) : ")
                if restart == 'n':
                    good = True

    camera.release()
    cv.destroyAllWindows()
create_collection_folder()


word = input('Enter word to manually collect : ')
start_collection(word)