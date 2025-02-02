import  cv2         as cv
import  numpy       as np
import  mediapipe   as mp
import  os
import  time
from    matplotlib  import  pyplot  as plt
from    tensorflow.keras.models import load_model
from text_to_speech import text_to_audio


# Models to detect limbs and draw on screen
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
    mp_d.draw_landmarks( image, results.face_landmarks,         mp_h.FACEMESH_CONTOURS)
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

    return np.concatenate([pose, left_h, right_h])


model = load_model('/Users/asmaeloulidi/Desktop/Hackathon 2025/asl-bridge/model-training/new.keras')



sample = []
sentence = []
t = 0.7
last_spoken_time = time.time()  # Track when the last audio was played
speak_interval = 2  # Speak the same word every 3 seconds


# words = ['none', 'person', 'hello', 'school', 'i love you']
words = ['none', 'person', 'hello']

# 0: iPhone, 1: webcam
capture = cv.VideoCapture(0)

with mp_h.Holistic(min_detection_confidence=0.7, min_tracking_confidence=0.7) as holistic:
    while capture.isOpened():
        _, frame = capture.read()
        image, results = mediapipe_detection(frame, holistic)
        draw_skeleton(image, results)
        data = transform_data(results)
        sample.append(data)
        sample = sample[-30:]
        
        if len(sample) == 30:
            result = model.predict(np.expand_dims(sample, axis=0))[0]
            predicted_word = words[np.argmax(result)]
            print(predicted_word)
            
            current_time = time.time()
            if current_time - last_spoken_time > speak_interval:
                text_to_audio(predicted_word)
                last_spoken_time = current_time

        cv.rectangle(image, (0,0), (640,640), (245,117, 16), -1)
        # cv.putText(image, ' '.join(sentence), (3,30), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv.LINE_AA)

        cv.imshow("ASL", image)
        if cv.waitKey(10) & 0xFF == ord('q'):
            break

capture.release()
cv.destroyAllWindows()