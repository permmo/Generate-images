import Functions


def SaltPapperFilter(PathOfImage,density):

    #nacitanie obrazka
    img = Functions.ReadImage(PathOfImage)

    # orezanie obrazka na stvorec, najpr sa zisitia suradnice tvare aby sa neorezala a urobi sa stvorec z obrazka
    # zistenie novych suradnic tvare
    CoordinatesOfFace = Functions.GetFaceCoordinates(img);
    img= Functions.CreateSquareImage(img, CoordinatesOfFace)

    #funckia SaltPepperFilter aplikuje salt-pepper filter
    noise_img = Functions.SaltPeperFilter(img,density);

    return noise_img;


