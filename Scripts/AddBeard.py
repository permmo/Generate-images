import cv2
import Functions


def AddBread(PathOfImage):

    #nacitanie obrazka a nacitanie brady
    img2 = cv2.imread('../Images/bread.jpg')
    img = Functions.ReadImage(PathOfImage)

    # orezanie obrazka na stvorec, najpr sa zisitia suradnice tvare aby sa neorezala a urobi sa stvorec z obrazka
    # zistenie novych suradnic tvare
    CoordinatesOfFace = Functions.GetFaceCoordinates(img);
    img = Functions.CreateSquareImage(img, CoordinatesOfFace)
    CoordinatesOfFace = Functions.GetFaceCoordinates(img);

    #vyrezanie tvare
    for (x, y, w, h) in CoordinatesOfFace:
        roi_img = img[y:y + h, x:x + w]

    #zistenie suradnic oci
    eyeCoordinates = Functions.GetEyesCoordinates(roi_img);
    eyeCoordinates = Functions.DeleteEyesNoise(eyeCoordinates);


    tmp = 0;
    tmpp = img.shape[0]

    #zistenie stredu oci, ktore budu pouzite pri polohovani brady
    #zistenie suradnic laveho oka, okolo ktoreho sa bude otacat obrazok
    for (ex, ey, ew, eh) in eyeCoordinates:
        if tmpp > ex + ew:
            tmpp = ex + ew
            leftEye1 = [ex + (ew / 2) + x, ey + (eh / 2) + y]
        tmp = tmp + ey + eh / 2
    tmp = tmp / 2 + y;
    tmp = int(tmp * 0.953800298063);

    #zistenie uhla o ktoreho je potrebne otocit obrazok
    #otocenie obrazka
    angle = Functions.GetAngleBetween2Eyes(eyeCoordinates);
    img = Functions.RotateImage(img, -angle, leftEye1[0], leftEye1[1])

    #vypocet pomeru
    #zvacsenie alebo zmensenie brady
    pomer = w * 0.86 / float(img2.shape[1]);
    newx = img2.shape[1] * pomer
    newy = img2.shape[0] * pomer
    resized = cv2.resize(img2, (int(newx), int(newy)))
    img2 = resized

    #vypocitanie y-lonovej suradnice pre polohu brady
    tmp2 = x+w/2 - img2.shape[0]/2
    tmp2 = round(tmp2 *0.948792569659);

    #suradnice pre ulozenie brady
    x = tmp
    y = tmp2;

    # Pridanie brady na obrazok
    rows, cols, channels = img2.shape
    roi = img[x:rows + x, y:cols + y]
    # Now create a mask of logo and create its inverse mask also
    img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    # Now black-out the area of logo in ROI
    img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
    # Take only region of logo from logo image.
    img2_fg = cv2.bitwise_and(img2, img2, mask=mask)
    # Put logo in ROI and modify the main image
    dst = cv2.add(img1_bg, img2_fg)
    img[x:rows + x, y:cols + y] = dst

    return img

