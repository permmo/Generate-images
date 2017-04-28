import Functions

def RotateImage(PathOfImage, angle):

    #nacitanie obrazka
    img = Functions.ReadImage(PathOfImage)

    # orezanie obrazka na stvorec, najpr sa zisitia suradnice tvare aby sa neorezala a urobi sa stvorec z obrazka
    # zistenie novych suradnic tvare
    CoordinatesOfFace = Functions.GetFaceCoordinates(img);
    img = Functions.CreateSquareImage(img, CoordinatesOfFace);

    #funkcia RotateImage otoci obrazok o zadany uhol
    rotateImg = Functions.RotateImage(img, angle, img.shape[0]/2,img.shape[1]/2);

    return rotateImg;



