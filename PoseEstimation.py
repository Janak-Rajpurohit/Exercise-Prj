import cv2 
import mediapipe as mp
import time
import math

class PoseDetector():

    def __init__(self, mode=False, upBody=False, smooth = True, detectionCon=0.5, trackCon=0.5 ):
        self.mode = mode
        self.upBody = upBody
        self.smooth =  smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpPose=mp.solutions.pose
        self.pose  = self.mpPose.Pose(self.mode, self.upBody, self.smooth, min_detection_confidence=self.detectionCon, min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findPose(self,img, draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        # print(results.pose_landmarks) 
        if self.results.pose_landmarks:  #if landmark detected
            if draw:
                self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return img
    
    def findPosition(self,img,draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for  id, lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w) , int(lm.y*h)  #cause landmarks are ratio of position and image dimension
                self.lmList.append([id,cx,cy])

                if draw:
                    cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED)
        return self.lmList
    
    def findAngle(self, img, p1, p2, p3, draw=True):
        x1,y1 = self.lmList[p1][1:]  #taking values from lm list by p1 p2 p3 index points of out body points
        x2,y2 = self.lmList[p2][1:]
        x3,y3 = self.lmList[p3][1:]
        
        # angle
        angle = math.degrees(math.atan2(y3-y2,x3-x2) - math.atan2(y1-y2,x1-x2))   #gives us angle in radian then convert to degree
        if angle<0:
            angle+=360
        # print(angle)
        # drawing points 
        if draw:
            cv2.line(img,(x1,y1),(x2,y2),(255,255,255),3)
            cv2.line(img,(x3,y3),(x2,y2),(255,255,255),3)

            cv2.circle(img, (x1,y1), 7, (0,0,255), cv2.FILLED)
            cv2.circle(img, (x1,y1), 12, (0,0,255), 2)
            cv2.circle(img, (x2,y2), 7, (0,0,255), cv2.FILLED)
            cv2.circle(img, (x2,y2), 12, (0,0,255), 2)
            cv2.circle(img, (x3,y3), 7, (0,0,255), cv2.FILLED)
            cv2.circle(img, (x3,y3), 12, (0,0,255), 2)
            cv2.putText(img, f"{int(angle)}", (x2-20,y2+50), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255), 2)
        return angle
    

def main():
    cap = cv2.VideoCapture(0)
    detector = PoseDetector()
    ptime=0
    while True:
        success, img = cap.read()

        img = detector.findPose(img)
        lmlist = detector.findPosition(img)
        if(len(lmlist)!=0):
            print(lmlist[14])

        #frame rate
        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime

        cv2.putText(img, f"FPS-{str(int(fps))}",(70,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        cv2.imshow("Image",img)
        cv2.waitKey(1)

if __name__ == "__main__":
    # main()
    pass