import cv2, urllib, Image, time, pyglet, sys, os
from subprocess import call


backsub = cv2.BackgroundSubtractorMOG()
#alarmSound = pyglet.resource.media("alarm.wav", streaming = False)
imgURL = sys.argv[1] # for instance via ip cam app
alarm = False

while True:
	filename = time.strftime("%Y%m%d%H%M%S.jpg", time.localtime()) # save image every 1 second
	urllib.urlretrieve(imgURL,filename)
	img = cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE);
	fgmask = backsub.apply(img,None, 0.01)
	contours = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	for contour in contours[0]:
		(x,y,w,h) = cv2.boundingRect(contour)
		if w > 10 and h > 10:
			cv2.rectangle(img, (x,y), (x+w,y+h), (255, 0, 0), 2)
			if not alarm:
				os.system("mplayer alarm.wav < /dev/null &")
				alarm = True
			#call(["mplayer", "alarm.wav"])
			#alarmSound.play()
	
	cv2.imshow("image", img)
	cv2.waitKey(1)
