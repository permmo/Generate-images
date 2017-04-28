import cv2
import Functions

def GaussFilter(PathOfImage,matrix):

    #nacitanie obrazka
    img = Functions.ReadImage(PathOfImage)

    # orezanie obrazka na stvorec, najpr sa zisitia suradnice tvare aby sa neorezala a urobi sa stvorec z obrazka
    # zistenie novych suradnic tvare
    CoordinatesOfFace = Functions.GetFaceCoordinates(img);
    img= Functions.CreateSquareImage(img, CoordinatesOfFace)

    #pouzitie funkcie GaussianBlur aplikuje gaussovov filter
    imgBlurred = cv2.GaussianBlur(img, (matrix, matrix), 0)

    return imgBlurred


