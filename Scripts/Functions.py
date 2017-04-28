import cv2
import os
import numpy as np
import random
import math

#najde tvar/e na obrazku
def GetFaceCoordinates (img):
    face_cascade = cv2.CascadeClassifier('..\Haar\haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    facesCoordinates = face_cascade.detectMultiScale(gray, 1.3, 5)
    facesCoordinates = DeleteFaceNoise(facesCoordinates)

    return facesCoordinates

#najde oci na obrazky
def GetEyesCoordinates(Image):
    eye_cascade = cv2.CascadeClassifier('..\Haar\haarcascade_eye.xml')
    grayImg = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
    eyesCoordinates = eye_cascade.detectMultiScale(grayImg)

    return eyesCoordinates

#vytvori stvorec z obrazka
#vytvori ho tak aby sa neorezala tvar
def CreateSquareImage (Img, FaceCoorditnates):
    yImage = Img.shape[0];
    xImage = Img.shape[1];

    img  = Img
    if(len(FaceCoorditnates[0]) > 2 ):
        (xFace, yFace, wFace, hFace) = FaceCoorditnates[0]
    else:
       return Img;

    cutPart = yImage-xImage;
    halfOfCutPart = cutPart/2;
    canBeCutedPart = yImage-hFace;

    if canBeCutedPart > cutPart: # ak cast ktora moze byt odrezana je vacsia ako cast ktoru chceme odrezat
        if(yFace > cutPart/2):  #ak na zaciatku fotky je vacsia cast ako polovica casti ktoru chceme odrezat
            if(yImage-(yFace+hFace) > cutPart/2):  # ak na konci fotky je vacsia cast ako polovica casti ktory chceme odrezat
                newImg = img[cutPart / 2:yImage-cutPart/2, 0:xImage]
            else: # ak  nieje tak musime zbytok ktory sme neodrezali odrezat zo zaciatku
                remainder = cutPart / 2 - (yImage-(yFace+hFace));
                newImg = img[(cutPart / 2) + remainder:yImage - (cutPart / 2)+ remainder , 0:xImage]
        else: #ak nieje tak musime zbytok ktory sme odrezali odrezat z konca
            remainder = cutPart/2 - yFace;
            newImg = img[(cutPart / 2) - remainder:yImage - (cutPart / 2) - remainder, 0:xImage]
    else:
        print()

    return newImg;

#nacita obrazok
def ReadImage(PathOfImage):
    imgOriginal = cv2.imread(PathOfImage)  # open image
    if imgOriginal is None:  # if image was not read successfully
        print "error: image not read from file \n\n"  # print error message to std out
        print PathOfImage;
        os.system("pause")  # pause so user can see error message
        return  # and exit function (which exits program)
    else:
        return imgOriginal;

#aplikuje sa salt-pepper filter
def SaltPeperFilter(image,prob):
    # image = ReadImage(PathOfImage)
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

#otoci obrazok
def RotateImage(image, angle):
    scale = 1.0
    (h, w) = image.shape[:2]
    x = w/2;
    y = h/2;
    center = (x,y);
    if center is None:
        center = (w / 2, h / 2)
    print center
    # Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    return rotated

#vyberie len 2 prave oci
def DeleteEyesNoise (EyesCoordinates):

    max1= 0;
    max2= 0;

    result = [0,0]

    for (ex, ey, ew, eh) in EyesCoordinates:
        if((ew*eh)>max1):
            max2= max1
            max1 = ew*eh
            result[1] = result[0]
            result[0] = [ex,ey,ew,eh]
        elif((ew*eh)>max2):
            max2 = ew * eh
            result[1] = [ex, ey, ew, eh]
    return result

#vyberie len jednu pravu tvar
def DeleteFaceNoise (FaceCoorditnates):
    max1 = 0;
    result = [1]
    for (x, y, w, h) in FaceCoorditnates:
        if((w*h)>max1):
            max1 = w*h
            result[0] = [x,y,w,h]

    return result

#zisti vzdialenost medzi ocami
def GetDistenceBetweenEyes(EyeCoordinates):
    if(len(EyeCoordinates) != 2):
        print "Delete noise in eyesCoordinates"
        return
    else:
       distance =(EyeCoordinates[1][0] + EyeCoordinates[1][3]/2) - (EyeCoordinates[0][0] + EyeCoordinates[0][2]/2)
       return abs(distance)

#zisti aky je potrebny uhol pre otocenie medzi 4 ocami
def GetAngleBetween4Eyes(EyeCoordinatesA, EyeCoordinatesB):

    if EyeCoordinatesA[0][0] < EyeCoordinatesA[1][0]:
        leftEye1= [EyeCoordinatesA[0][0]+EyeCoordinatesA[0][1]/2,EyeCoordinatesA[0][1]+EyeCoordinatesA[0][3]/2]
        rightEye1 = [EyeCoordinatesA[1][0]+EyeCoordinatesA[1][1]/2,EyeCoordinatesA[1][1]+EyeCoordinatesA[1][3]/2]
    else:
        rightEye1 = [EyeCoordinatesA[0][0] + EyeCoordinatesA[0][1] / 2,
                    EyeCoordinatesA[0][1] + EyeCoordinatesA[0][3] / 2]
        leftEye1 = [EyeCoordinatesA[1][0] + EyeCoordinatesA[1][1] / 2,
                     EyeCoordinatesA[1][1] + EyeCoordinatesA[1][3] / 2]

    if EyeCoordinatesB[0][0] < EyeCoordinatesB[1][0]:
        leftEye2 = [EyeCoordinatesB[0][0] + EyeCoordinatesB[0][1] / 2,
                    EyeCoordinatesB[0][1] + EyeCoordinatesB[0][3] / 2]
        rightEye2 = [EyeCoordinatesB[1][0] + EyeCoordinatesB[1][1] / 2,
                     EyeCoordinatesB[1][1] + EyeCoordinatesB[1][3] / 2]
    else:
        rightEye2 = [EyeCoordinatesB[0][0] + EyeCoordinatesB[0][1] / 2,
                     EyeCoordinatesB[0][1] + EyeCoordinatesB[0][3] / 2]
        leftEye2 = [EyeCoordinatesB[1][0] + EyeCoordinatesB[1][1] / 2,
                    EyeCoordinatesB[1][1] + EyeCoordinatesB[1][3] / 2]

    tmp = leftEye1[0] - leftEye2[0];
    if tmp > 0:
        leftEye2[0]= leftEye2[0]+tmp
        rightEye2[0]=rightEye2[0]+tmp
    else:
        tmp = tmp * (-1)
        leftEye1[0] = leftEye1[0]+tmp
        rightEye1[0]=rightEye1[0]+tmp

    tmp = leftEye1[1] - leftEye2[1]
    if tmp > 0:
        leftEye2[1]= leftEye2[1]+tmp
        rightEye2[1]=rightEye2[1]+tmp

    else:
        tmp = tmp * (-1)
        leftEye1[1] = leftEye1[1]+tmp
        rightEye1[1]=rightEye1[1]+tmp


    rightEye1[0] = rightEye1[0] -leftEye1[0]
    rightEye1[1] = rightEye1[1] -leftEye1[1]
    rightEye2[0] = rightEye2[0] - leftEye2[0]
    rightEye2[1] = rightEye2[1] - leftEye2[1]

    x = (rightEye1[0]*rightEye2[0]) + (rightEye1[1]*rightEye2[1])
    y = (math.sqrt(math.pow(rightEye1[0],2)+ math.pow(rightEye1[1],2)))
    z = (math.sqrt(math.pow(rightEye2[0],2)+ math.pow(rightEye2[1],2)))
    if(y == z):
        result = 0;
    else:
        result= math.degrees(math.acos((x/(y*z))))
    return result

# otoci obrazok o zadany uhol, okolo zadanych suradnic
def RotateImage(image, angle, x,y, scale = 1.0):
    (h, w) = image.shape[:2]
    center = (x,y);
    if center is None:
        center = (w / 2, h / 2)
    # Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    return rotated

#zisti aky je potrebny uhol pre otocenie medzi 2 ocami
def GetAngleBetween2Eyes(EyeCoordinatesA):
    if EyeCoordinatesA[0][0] < EyeCoordinatesA[1][0]:
        leftEye1 = [EyeCoordinatesA[0][0] + EyeCoordinatesA[0][1] / 2,
                    EyeCoordinatesA[0][1] + EyeCoordinatesA[0][3] / 2]
        rightEye1 = [EyeCoordinatesA[1][0] + EyeCoordinatesA[1][1] / 2,
                     EyeCoordinatesA[1][1] + EyeCoordinatesA[1][3] / 2]
    else:
        rightEye1 = [EyeCoordinatesA[0][0] + EyeCoordinatesA[0][1] / 2,
                     EyeCoordinatesA[0][1] + EyeCoordinatesA[0][3] / 2]
        leftEye1 = [EyeCoordinatesA[1][0] + EyeCoordinatesA[1][1] / 2,
                    EyeCoordinatesA[1][1] + EyeCoordinatesA[1][3] / 2]

    a = leftEye1[1] - rightEye1[1];
    b = leftEye1[0] - rightEye1[0];
    c = math.sqrt(math.pow(a,2)+math.pow(b,2));
    result = math.degrees(math.asin((a / c)))
    return result;