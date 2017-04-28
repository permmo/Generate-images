import cv2
import Functions


def Merge2Imges(PathOfImage,weight):

    #nacitanie zakladneho obrazka na prekrytie
    img = cv2.imread('../Images/img1.jpg')

    #nacitanie obrazka
    img2 = Functions.ReadImage(PathOfImage)

    ################################################################
    #Defaultny obrazok
    ################################################################


    # orezanie obrazka na stvorec, najpr sa zisitia suradnice tvare aby sa neorezala a urobi sa stvorec z obrazka
    # funkcia DeleteFaceNoise vyberie len jednu pravu tvar
    CoordinatesOfFace = Functions.GetFaceCoordinates(img);
    img = Functions.CreateSquareImage(img, CoordinatesOfFace)
    CoordinatesOfFace = Functions.GetFaceCoordinates(img);

    #vyrezanie tvare
    for (x, y, w, h) in CoordinatesOfFace:
        roi_img = img[y:y + h, x:x + w]

    #zistenie suradnic oci
    eyeCoordinates = Functions.GetEyesCoordinates(roi_img);
    eyeCoordinates = Functions.DeleteEyesNoise(eyeCoordinates);

    #zistenie vzdialenosti oci
    distance1 = Functions.GetDistenceBetweenEyes(eyeCoordinates)

    #zistenie suradnic laveho oka
    tmp = img.shape[0]
    for (ex, ey, ew, eh) in eyeCoordinates:
        if tmp > ex+ew :
            tmp =ex+ ew
            leftEye1 = [ex+(ew/2)+x, ey+(eh/2)+y]



    ################################################################
    # 2. Obrazok
    ################################################################

    # orezanie obrazka na stvorec, najpr sa zisitia suradnice tvare aby sa neorezala a urobi sa stvorec z obrazka
    # zistenie novych suradnic tvare
    CoordinatesOfFace = Functions.GetFaceCoordinates(img2);
    img2 = Functions.CreateSquareImage(img2, CoordinatesOfFace)
    CoordinatesOfFace = Functions.GetFaceCoordinates(img2);

    #vyrezanie tvare
    for (x, y, w, h) in CoordinatesOfFace:
        roi_img2 = img2[y:y + h, x:x + w]

    #zistenie suradnic oci
    eyeCoordinates2 = Functions.GetEyesCoordinates(roi_img2);
    eyeCoordinates2 = Functions.DeleteEyesNoise(eyeCoordinates2);

    #zistenie vzdialenosti oci
    distance2 = Functions.GetDistenceBetweenEyes(eyeCoordinates2)

    #zistenie suradnic laveho oka
    tmp = img2.shape[0]
    for (ex, ey, ew, eh) in eyeCoordinates2:
        if tmp >ex+ ew:
            tmp  = ex+ ew
            leftEye2 = [ex + (ew / 2)+x, ey + (eh / 2)+y]


    ################################################################
    # Prekrytie
    ################################################################

    #vypocet pomeru
    #zvacsenie alebo zmensenie obrazka
    pomer  =  distance1/float(distance2)
    newx = img2.shape[1] * pomer
    newy = img2.shape[0] * pomer
    leftEye2 = [int(i * pomer) for i in leftEye2]
    img2 = cv2.resize(img2, (int(newx), int(newy)))

    # zistenie uhla o ktoreho je potrebne otocit obrazok
    # otocenie obrazka
    angle = Functions.GetAngleBetween4Eyes(eyeCoordinates, eyeCoordinates2)
    img = Functions.RotateImage(img, -angle, leftEye1[0], leftEye1[1])



    #umiestnenie obrazka 2
    #orezanie ak je potrebne
    odchylka_x = leftEye1[0] - leftEye2[0]
    odchylka_y = leftEye1[1] - leftEye2[1]
    if odchylka_x > 0:
        img = img[0:0+img.shape[0], odchylka_x:odchylka_x+img.shape[1]]
    else:
        odchylka_x = odchylka_x * (-1)
        img2 = img2[0:0+img2.shape[0], odchylka_x:odchylka_x+img2.shape[1]]

    if odchylka_y > 0:
        img = img[odchylka_y:odchylka_y+img.shape[0], 0:0+img.shape[1]]
    else:
        odchylka_y = odchylka_y * (-1)
        img2 = img2[odchylka_y:odchylka_y+img2.shape[0], 0:0+img2.shape[1]]

    if img.shape[0] >= img2.shape[0]:
        img= img[0:0+img2.shape[0], 0:0+img.shape[1]]
    else:
        img2= img2[0:0+img.shape[0], 0:0+img.shape[1]]

    if img.shape[1] > img2.shape[1]:
        img = img[0:0+img.shape[0], 0:0+img2.shape[1]]
    else:
        img2 = img2[0:0+img2.shape[0],0:+img.shape[1]]


    #funkcia addWeighted prekryje 2 obrazky
    merge_img = cv2.addWeighted(img2, weight, img, 1-weight, 0)

    return  merge_img

