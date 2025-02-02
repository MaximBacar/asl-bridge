import  cv2         as cv
import  numpy       as np
import  mediapipe   as mp

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