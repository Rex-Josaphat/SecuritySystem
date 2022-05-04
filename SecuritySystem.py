# Import modules
import cv2
import time
import datetime

cap  = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

'''Video recording and saving'''
detection = False
detection_stopped_time = None
timer_started = False
Seconds_to_record_after_detection = 5

frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Four character code (Video Format)

while True:
    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    bodies = body_cascade.detectMultiScale(gray, 1.1, 5)

    if len(faces) + len(bodies) > 0:
        if detection:
            timer_started = False
        else:
            detection = True
            current_time =  datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S') # Give out the currrent time
            outputV = cv2.VideoWriter(f'{current_time}.mp4', fourcc, 20, frame_size) # Saving recorded video
            print('Started Recording!')
    elif detection:
        if timer_started:
            '''If recording has started, check the amount of time no object is detected so as to stop the video'''
            if time.time() - detection_stopped_time >= Seconds_to_record_after_detection: 
                detection = False
                timer_started = False
                outputV.release()
                print('Stopped Reecording!')
        else:
            timer_started = True
            detection_stopped_time = time.time()

    if detection:
        outputV.write(frame)

    for (x, y, width, height) in faces:
        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 3)
    
    cv2.imshow('Security Camera', frame)

    if cv2.waitKey(1) == ord('q'):
        break
    
outputV.release()
cap.release()
cv2.destroyAllWindows()
