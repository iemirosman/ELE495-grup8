import cv2
import numpy as np
import serial
import time
import pigpio
import imutils
from imutils.video import WebcamVideoStream
from imutils.video import FPS
from PIL import Image, ImageTk
from ControlPanel import ControlPanel
GPIO=pigpio.pi()

cap = cv2.VideoCapture(0)

ctrlPnl = ControlPanel("tenis")
mainWindow = ctrlPnl.openControlPanel()

cap.set(3,640)
cap.set(4,480)

print(cap.get(3))
print(cap.get(4))

ScaleCoef = 25/150

##pid
servoPIN = 12
servoPIN2 = 13
GPIO.set_mode(12,pigpio.OUTPUT)
GPIO.set_mode(13,pigpio.OUTPUT)
GPIO.set_PWM_frequency(12,50)
GPIO.set_PWM_frequency(13,50)

GPIO.hardware_PWM(12,50,75000)
GPIO.hardware_PWM(13,50,75000)

totalErrorX=0
totalErrorY=0
timeInterval=1
alpha,beta,prevalpha,prevBeta= 0,0,0,0
N=20
prevDerivX=0
prevDerivY=0
prevIntegX=0
prevIntegY=0
prevErrorX=0
prevErrorY=0
delivery_time=0
doksanX=7.5 #siyah top 7.5
doksanY=7.5 #siyah top 7.5
pre_servo_out1 = 0
pre_servo_out2 = 0

rad=ctrlPnl.getSize() # siyah top 3 #tenis topu 6



###
def PIDcontrol(ballPosX, ballPosY, prevBallPosX, prevBallPosY, refX, refY, Kp_PID, Ki_PID, Kd_PID, Lp, Li, Ld):     # PID controller
    global totalErrorX, totalErrorY
    global alpha, beta, prevAlpha, prevBeta
    global pre_servo_out1
    global pre_servo_out2
    global Ts, delivery_time, N
    global prevDerivX, prevDerivY, prevIntegX, prevIntegY
    global prevErrorX, prevErrorY

    Ts = time.time() - delivery_time    #sampling time
    delivery_time = time.time()
    
    #print("Time:" + str(Ts))
    #print("Time:" + str(delivery_time))

    errorX = refX - ballPosX
    errorY = refY - ballPosY


    #Kp = sliderCoefP.get()
    #Ki = sliderCoefI.get()
    #Kd = sliderCoefD.get()
    #Kp=Kp_PID
    #Ki=Ki_PID
    #Kd=Kd_PID
    
    
    if (abs(ballPosX) <= rad and abs(ballPosY) <= rad): # buyuk top 6 #kucuk top 4
        flagM=1
        Kp=Kp_PID
        Ki=Ki_PID
        Kd=Kd_PID

    else:

        Kp=Lp #3 # siyah 3 #beyaz top 3 # tenis topu 2
        Ki=Li #0   # siyah top 0.01 3 beyaz top 0.01 3 tenis ki 0.2
        Kd=Ld #2.5  # siyah top 2.5 # beyaz top 2.5 # tenis topu 2.5

        #Kp=2
        #Ki=0.1
        #Kd=2
       
    try:
        derivX = (prevBallPosX - ballPosX) / Ts
    except ZeroDivisionError:
        derivX = 0

    try:
        derivY = (prevBallPosY - ballPosY) / Ts
    except ZeroDivisionError:
        derivY = 0

    Cix = prevIntegX + errorX*Ki*0.1                    #Ki * totalErrorX
    Ciy = prevIntegY + errorY*Ki*0.1                    #Ki * totalErrorX
    print("PrevIntegX: "+str(prevIntegX) + " PrevIntegY: " + str(prevIntegY))

    #if errorX==refX and errorY==refY:
        #Cix=0
        #Ciy=0


    Cdx =  Ts/(1+N*Ts)*(N*Kd*derivX + prevDerivX/Ts) #(Kd*N*(errorX-prevErrorX)+prevDerivX)/(1+N*Ts)# #Kd * ((errorX - prevErrorX)/Ts)
    Cdy =  Ts/(1+N*Ts)*(N*Kd*derivY + prevDerivY/Ts) #(Kd*N*(errorY-prevErrorY)+prevDerivY)/(1+N*Ts)# #Kd * ((errorY - prevErrorY)/Ts)

    print("PrevDerivX: "+str(prevDerivX) + " PrevDerivY: " + str(prevDerivY))

    Ix = Kp * errorX + Cix + Cdx
    Iy = Kp * errorY + Ciy + Cdy

    Ix = round(Ix, 3)
    Iy = round(Iy, 3)
    print("Ix: "+str(Ix)+" Iy: "+str(Iy))
    print("exP: "+str(Kp*errorX)+ " exI: "+str(Cix)+" exD: "+str(Cdx))
    print("eyP: "+str(Kp*errorY)+ " eyI: "+str(Ciy)+" eyD: "+str(Cdy))
    
    max_alpha=45

    if Ix > max_alpha:
        Ix = max_alpha
    elif Ix < - max_alpha:
        Ix = - max_alpha
    if Iy > max_alpha:
        Iy = max_alpha
    elif Iy < - max_alpha:
        Iy = - max_alpha

    prevIntegY = Ciy
    prevIntegX = Cix
    prevDerivX = derivX
    prevDerivY = derivY
    flagM=1
    print("Kp: " + str(Kp) + " Ki: " + str(Ki) + " Kd: " + str(Kd))
            
       
    print(totalErrorX)
    
    
    servo_out1= Ix/22.5 +doksanX  #6.5
    servo_out2= Iy/22.5 +doksanY  #6.5
    servo_out1=servo_out1*10000
    servo_out2=servo_out2*10000

    if (abs(ballPosX) <= rad/2 and abs(ballPosY) <= rad/2 ): # buyuk top 3 #kucuk top 2 #rad/2
        servo_out1 = doksanX*10000
        servo_out2 = doksanY*10000
        
    #elif (abs(ballPosX) < 6 and abs(ballPosY) < 6):
        #servo_out1 = 0.8*servo_out1 + 0.2*pre_servo_out1
        #servo_out2 = 0.8*servo_out2 + 0.2*pre_servo_out2

    #pre_servo_out1 = servo_out1
    #pre_servo_out2 = servo_out2
        
    
    GPIO.hardware_PWM(servoPIN,50,int(servo_out1))
    GPIO.hardware_PWM(servoPIN2,50,int(servo_out2))
    
    print("ServoX: " + str(servo_out1) + "\n" + "ServoY: "+str(servo_out2))

qprevRefX, prevRefY = 0, 0
start_time = 0


###pid


def writeToLCD (x,y,IsBallDetected):
    num_x = str(x)
    num_y = str(y)
    flag = str(IsBallDetected)
    ser = serial.Serial('/dev/rfcomm0', 9600)
    ser.write(str.encode(num_x))
    ser.write(str.encode(' '))
    ser.write(str.encode(num_y))
    ser.write(str.encode(' '))
    ser.write(str.encode(flag))
    
    return


def grab_contours(cnts):
    
    if len(cnts) == 2:
        cnts = cnts[0]

    elif len(cnts) == 3:
        cnts = cnts[1]
        
    else:
        raise Exception(("Contours tuple must have length 2 or 3, "
            "otherwise OpenCV changed their cv2.findContours return "
            "signature yet again. Refer to OpenCV's documentation "
            "in that case"))

    return cnts

def nothing (x):
    pass

#agir sari   #golf #agir sari gece #pembe # mavi # beyaz gece # agir siyah # yeşil küçük # kırmızı #tenis #beyaz gunduz 
#0           13     29              54      54      33          0           39           0          0       20
#92          95     144             68      64      5           0           46           157        78      5
#178         175    122             160     87      228         77          0            0          178     196
#175         186    59              255     255     96          75          76           255        275     114
#200         200    255             255     255     98          164         179          209        200     98
#255         255    255             255     255     255         255         255          255        255     255


##cv2.namedWindow ("Top Rengi/Boyutu Ayarla")#agir sari top 0 #golf topu 13 #turuncu golf topu ile aynı
##                                                                            #agir sari   #golf #agir sari gece #pembe # mavi # beyaz # agir siyah # yeşil küçük # kırmızı #tenis
##cv2.createTrackbar("Lower_H", "Top Rengi/Boyutu Ayarla", 39, 255, nothing)   #0           13     29              54      54      33      0           39           0          0
##cv2.createTrackbar("Lower_S", "Top Rengi/Boyutu Ayarla", 46, 255, nothing)   #92          95     144             68      64      5       0           46           157        78
##cv2.createTrackbar("Lower_V", "Top Rengi/Boyutu Ayarla", 0, 255, nothing)   #178         175    122             160     87      228     77          0            0          178
##cv2.createTrackbar("Upper_H", "Top Rengi/Boyutu Ayarla", 76, 255, nothing)   #175         186    59              255     255     96      75          76           255        275
##cv2.createTrackbar("Upper_S", "Top Rengi/Boyutu Ayarla", 179, 255, nothing)  #200         200    255             255     255     98      164         179          209        200
##cv2.createTrackbar("Upper_V", "Top Rengi/Boyutu Ayarla", 255, 255, nothing)  #255         255    255             255     255     255     255         255          255        255
##cv2.createTrackbar("Min_Radius", "Top Rengi/Boyutu Ayarla", 10, 255, nothing)
##cv2.createTrackbar("Max_Radius", "Top Rengi/Boyutu Ayarla", 50, 255, nothing)
##
##cv2.namedWindow ("PID Parametre Ayarla")
##cv2.createTrackbar("Kp", "PID Parametre Ayarla", 93, 1000, nothing) #ilk deger 200 siyah top 215 # beyaz top 13  24       #yeşil top 93
##cv2.createTrackbar("Ki", "PID Parametre Ayarla", 25, 1000, nothing) #ilk deger 30 siyah top 110 # beyaz top 22    13                   0
##cv2.createTrackbar("Kd", "PID Parametre Ayarla", 162, 1000, nothing) #ilk deger 300 siyah top 300  # beyaz top 116   409             162
ScaleX = 0
ScaleY = 0
PID_Counter = 0
Servo_Counter = 0
ServoFlag = 1
IsBallDetected=0
PreX =0
PreY =0

showRawStream = ctrlPnl.camRawStream()
showMaskedStream = ctrlPnl.camMaskedStream()

def main():
    global PreX ,PreY, ScaleX, ScaleY

    ret, frame = cap.read()
    #frame = frame[20:440, 135:555]
    frame = imutils.resize(frame[20:440, 135:555], width = 300)
    blurred = cv2.GaussianBlur(frame, (11,11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
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
##
##    Ki = cv2.getTrackbarPos("Ki", "PID Parametre Ayarla")
##    Kp = cv2.getTrackbarPos("Kp", "PID Parametre Ayarla")
##    Kd = cv2.getTrackbarPos("Kd", "PID Parametre Ayarla")



    Kp, Ki, Kd = ctrlPnl.getInnerPID()
    Lp, Li, Ld = ctrlPnl.getOuterPID()

    hLower, hUpper = ctrlPnl.getH()
    sLower, sUpper = ctrlPnl.getS()
    vLower, vUpper = ctrlPnl.getV()

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

        cv2.circle(frame, (center[0], center[1]), 1, (0,255,0), 3)
        cv2.circle(frame, (center[0], center[1]), center[2], (0,0,255), 3)
        prevCircle = center
        ScaleX = int((center[0]-150)*ScaleCoef)
        ScaleY = int((center[1]-150)*ScaleCoef)
        ScaleCenter = [ScaleX, ScaleY]
        print(ScaleCenter)
        rX=0
        rY=0
        

        PIDcontrol(ScaleX,ScaleY,PreX,PreY,rX,rY,Kp,Ki,Kd, Lp, Li, Ld)
        PreX=ScaleX
        PreY=ScaleY
        noBallFlag=1
    else:
        noBallFlag=0
        IsBallDetected = 0
        #Servo1.ChangeDutyCycle(6.94) #levhaya gore doksana yakın
        #Servo2.ChangeDutyCycle(6.94)
        #Servo1.ChangeDutyCycle(0)
        #Servo2.ChangeDutyCycle(0)
    #cv2.imshow('Frame',frame)
    #cv2.imshow('Mask',mask)
    print("Flag: " + str(IsBallDetected))
##    writeToLCD (ScaleX, ScaleY, IsBallDetected)


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

	
    if cv2.waitKey(1) & 0xFF == ord("q"):
        return



main()
mainWindow.mainloop()

cap.release()
cv2.destroyAllWindows()


   
