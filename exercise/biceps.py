
import cv2
import numpy as np
import time
from PoseEstimation import PoseDetector
cap = cv2.VideoCapture(0)

detector = PoseDetector()
class Biceps:
    def gen_frames():
        count = 0
        dir = 0  #up-0 or down-1

        while True:
            success,img = cap.read()
            # img = cv2.resize(img, (1000,700))

            img = detector.findPose(img,draw=False)
            lmlist = detector.findPosition(img,draw=False)
            if len(lmlist)!=0:
                # print(lmlist[14])
                # left arm
                # angle = detector.findAngle(img,12,14,16)
                # right arm
                angle = detector.findAngle(img,11,13,15)
                per = np.interp(angle,(50,160),(0,100))
                print(angle,per)

                #check for dumbble curls
                if per == 100:
                    if dir == 0:
                        count += 0.5
                        dir = 1  #change dir to down
                if per == 0:
                    if dir == 1:
                        count+=0.5
                        dir = 0   #change dir to up
            # cv2.rectangle(img, (30,100),(150,200),(218,155,47),cv2.FILLED)
            cv2.putText(img, f"Count-{int(count)}", (50,100), cv2.FONT_HERSHEY_PLAIN, 3, (255,110,110), 2)
            # cv2.imshow("Image",img)
            ret, buffer = cv2.imencode('.jpg', img)
            frame_bytes = buffer.tobytes()
                # if return is used then loop will stop and only 1 frame is return 
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            # cv2.waitKey(1)


