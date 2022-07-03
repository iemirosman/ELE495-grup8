import cv2
import numpy as np
from PIL import Image, ImageTk
from ControlPanel import ControlPanel


cap = cv2.VideoCapture(0)

#cap.set(3,640)
#cap.set(4,480)

#print(cap.get(3))
#print(cap.get(4))


class KalmanFilter:
    kf = cv2.KalmanFilter(4, 2)
    kf.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
    kf.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)


    def predict(self, coordX, coordY):
        ''' This function estimates the position of the object'''
        measured = np.array([[np.float32(coordX)], [np.float32(coordY)]])
        self.kf.correct(measured)
        predicted = self.kf.predict()
        x, y = int(predicted[0]), int(predicted[1])
        return x, y

def nothing (x):
    pass

ctrlPnl = ControlPanel("profile1")
mainWindow = ctrlPnl.openControlPanel()

##cv2.namedWindow ("Top Rengi/Boyutu Ayarla")
##cv2.createTrackbar("Lower_H", "Top Rengi/Boyutu Ayarla", 0, 255, nothing) #39
##cv2.createTrackbar("Lower_S", "Top Rengi/Boyutu Ayarla", 141, 255, nothing) #84
##cv2.createTrackbar("Lower_V", "Top Rengi/Boyutu Ayarla", 0, 255, nothing)  #0
##cv2.createTrackbar("Upper_H", "Top Rengi/Boyutu Ayarla", 28, 255, nothing)
##cv2.createTrackbar("Upper_S", "Top Rengi/Boyutu Ayarla", 255, 255, nothing)
##cv2.createTrackbar("Upper_V", "Top Rengi/Boyutu Ayarla", 255, 255, nothing)
##
##cv2.createTrackbar("Min_Radius", "Top Rengi/Boyutu Ayarla", 20, 255, nothing)
##cv2.createTrackbar("Max_Radius", "Top Rengi/Boyutu Ayarla", 30, 255, nothing)

kf = KalmanFilter()

showRawStream = ctrlPnl.camRawStream()
showMaskedStream = ctrlPnl.camMaskedStream()

def main():
    ret, frame = cap.read()
    frame = frame[10:470, 110:570]
    
    blurred = cv2.GaussianBlur(frame, (11,11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    hLower, hUpper = ctrlPnl.getH()
    sLower, sUpper = ctrlPnl.getS()
    vLower, vUpper = ctrlPnl.getV()
##    
##    l_h = cv2.getTrackbarPos("Lower_H", "Top Rengi/Boyutu Ayarla")
##    l_s = cv2.getTrackbarPos("Lower_S", "Top Rengi/Boyutu Ayarla")
##    l_v = cv2.getTrackbarPos("Lower_V", "Top Rengi/Boyutu Ayarla")
##	
##    u_h = cv2.getTrackbarPos("Upper_H", "Top Rengi/Boyutu Ayarla")
##    u_s = cv2.getTrackbarPos("Upper_S", "Top Rengi/Boyutu Ayarla")
##    u_v = cv2.getTrackbarPos("Upper_V", "Top Rengi/Boyutu Ayarla")
##
##    min_r = cv2.getTrackbarPos("Min_Radius", "Top Rengi/Boyutu Ayarla")
##    max_r = cv2.getTrackbarPos("Max_Radius", "Top Rengi/Boyutu Ayarla")

    min_r, max_r =  ctrlPnl.getRadius()
    
    l_b = np.array([hLower, sLower, vLower])
    u_b = np.array([hUpper, sUpper, vUpper])

    mask = cv2.inRange(hsv, l_b, u_b)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    #res = cv2.bitwise_and(frame, frame, mask)
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 2, 500, param1=300,
                               param2=10, minRadius=min_r, maxRadius=max_r)

    if type(circles) == np.ndarray and circles.size != 0:
        IsBallDetected=1
        circles = np.uint16(np.around(circles))
        center = None
        prevCircle = None
        for i in circles[0,:]:
            if center is None:
                center = i
            if prevCircle is not None:
                if dist (center[0], center[1], prevCircle[0], prevCircle[1]) <= dist(i[0], i[1], prevCircle[0], prevCircle[1]):
                     center = i

        predicted = kf.predict(center[0], center[1])
        
        cv2.circle(frame, (center[0], center[1]), 1, (0,255,0), 3)
        cv2.circle(frame, (center[0], center[1]), center[2], (0,0,255), 3)
        cv2.circle(frame, (predicted[0], predicted[1]), 20, (255, 0, 0), 4)
        cv2.circle(frame, (predicted[0], predicted[1]), 1, (0,0,255), 3)
        prevCircle = center

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=frame)
    showRawStream.imgtk = imgtk
    showRawStream.configure(image=imgtk)
    mask = Image.fromarray(mask)
    masktk = ImageTk.PhotoImage(image=mask)
    showMaskedStream.masktk = masktk
    showMaskedStream.configure(image=masktk)
    showMaskedStream.after(5, main)    
    
    
    
##    cv2.imshow('Frame',frame)
##    cv2.imshow('Mask',mask)
##
    if cv2.waitKey(1) & 0xFF == ord("q"):
        return

main()
mainWindow.mainloop()


cap.release()
cv2.destroyAllWindows()

