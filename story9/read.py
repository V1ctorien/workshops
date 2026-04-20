import cv2 as cv
import numpy as np

#------------------------------------rescale--------------------------------
# # def rescale(frame, scale=0.3):

#     width= int(frame.shape[1]*scale)
#     height= int(frame.shape[0]*scale)
#     dimensions= (width,height)

#     return cv.resize(frame,dimensions,interpolation=cv.INTER_AREA)


# def changeRes(vid,width,height):
#     vid.set(3,width)
#     vid.set(4,height)

#----------------lecture image-------------------------
img= cv.imread(r"photos\foret.jpg")

# cv.imshow('foret', img)

# cv.waitKey(0)
#------------------------lecture video---------------------------------
# vid=cv.VideoCapture(r"videos\videtest.mp4")

# while True:
#     isTrue, frame = vid.read()
#     fr_resize=rescale(frame)
#     cv.imshow('video', frame)
#     cv.imshow('scalevid',fr_resize)

#     if cv.waitKey(20) & 0xFF==ord('d'):
#         break

# vid.release()
# cv.destroyWindow()
# cv.waitKey(0)
#-----------------------------------------------------------------------------------------

#-------------------------blank image---------------------------------------
# blank= np.zeros((250,500,3), dtype="uint8") # np.zeros(taille axe y, taille  axe x, nb de couleurs )
# cv.imshow('blank',blank)
# blank[50:200, 30:40] = 245,186,15  #blank[range sur l'axe y, range sur l'axe x]= code couleur
# cv.imshow("test",blank)
# cv.waitKey(0)

# blank1=np.zeros((150,350,3), dtype='uint8')
# cv.rectangle(blank1,(50,10),(100,50),(159,45,250), thickness=cv.FILLED) #.rectangle(coordoeene en haut a gauche (x,y) , coordonnée en bas a droit , code couleur)
# #thickness (epaisseur)= cv.FILLED pour remplir le rectangle
# cv.imshow('rect',blank1)
# # cv.waitKey(0)

# cv.circle(blank1,(blank1.shape[1]//4,blank1.shape[0]//2),15,(159,45,250), thickness=5)
# cv.imshow('cercle', blank1)
# cv.waitKey(0)

gray= cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.imshow('gra',gray)
blur= cv.GaussianBlur(gray,(3,3),cv.BORDER_DEFAULT)
cv.imshow('blur',blur)
canny=cv.Canny(blur,125,175)
cv.imshow('cann',canny)
dilated=cv.dilate(canny,(7,7),iterations=2)
cv.imshow('dil', dilated)
cv.waitKey(0)