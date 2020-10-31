import sys
import cv2
from openalpr import Alpr
from filter import filter_mask
import os
import csv
import datetime


dst=os.getcwd()+'\cropedImages'         # destination to save the images
if not os.path.exists(dst):
    os.makedirs(dst)

fieldnames = ['ID', 'Plate number', 'Image Path','Date' , 'Time']
fileID=open('file.csv','w')       # file to save the data
newFileWriter = csv.writer(fileID)
newFileWriter.writerow(fieldnames)

alpr = Alpr("us","C:/Users/91620/Desktop/License Plate detection/ALPR--Automatic-License-Plate-Recognition-master/openalpr_64/runtime_data/config","C:/Users/91620/Desktop/License Plate detection/ALPR--Automatic-License-Plate-Recognition-master/openalpr_64/runtime_data")
alpr.set_top_n(10)
alpr.set_default_region("md")
if not alpr.is_loaded():
    sys.exit(1)

Video_Source='15ene2018.avi'
thrsArea=100000
print("Using OpenALPR " + alpr.get_version())
cap = cv2.VideoCapture(Video_Source)
bg_subtractor = cv2.createBackgroundSubtractorMOG2(
    history=500, detectShadows=True)

print ('Training BG Subtractor...')
cv2.namedWindow('op', cv2.WINDOW_NORMAL)
cnt=0
while True:
    ok,frame=cap.read()
    if not ok:

        sys.exit()
    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        Rfilter = cv2.bilateralFilter(gray, 9, 75, 75)

        # Threshold image
        ret, filtered = cv2.threshold(Rfilter, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        filtered = cv2.medianBlur(frame, 5)
        fg_mask = bg_subtractor.apply(filtered, None, 0.01)
        fg_mask = filter_mask(fg_mask)
        im, contours, hierarchy = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        cntr = []
        for contour in contours:
            contourSize = cv2.contourArea(contour)
            if (contourSize > int(thrsArea)):
                cntr.append(contour)
                cnt+=1

        for ii in range(0, len(cntr)):
            (x, y, w, h) = cv2.boundingRect(cntr[ii])

            cv2.rectangle(frame, (x, y), (x + w - 1, y + h - 1),
                          (0, 255, 0), 1)
            cropedframe=frame[y:y+h, x:x+w]
            filename=dst+'\\'+str(cnt)+'.jpg'
            cv2.imwrite(filename,cropedframe) # write the image

            ret, enc = cv2.imencode("*.bmp", cropedframe)
            results = alpr.recognize_array(bytes(bytearray(enc)))

            if results['results']:
                print('License plate Detected and Recorded')

                time = datetime.datetime.now().time()
                date = datetime.datetime.now().date()
                plateno = results['results'][0]['plate']
                confidance=results['results'][0]['confidence']
                print('Plate: ',plateno, 'Confidance: ',confidance)

                newFileWriter.writerow([cnt, str(plateno), filename, date, time]) # write the csv file


        cv2.imshow('op', frame)
        if cv2.waitKey(33) == 27:
            break
